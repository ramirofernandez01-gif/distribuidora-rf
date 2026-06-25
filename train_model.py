from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from joblib import dump
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import numpy as np

positivos = [
    "el sistema funciona perfectamente", "me encanta la nueva funcionalidad", "excelente soporte técnico",
    "gran experiencia de usuario", "la integración es perfecta", "la aplicación es muy intuitiva",
    "la velocidad de respuesta es impresionante", "el equipo resolvió mi problema rápidamente",
    "la interfaz es moderna y atractiva", "cumple todas mis expectativas", "experiencia muy positiva",
    "el diseño es simple y efectivo", "muy útil para mi trabajo", "documentación completa y clara",
    "la funcionalidad de búsqueda es excelente", "producto de alta calidad totalmente recomendado",
    "superó todas mis expectativas", "servicio al cliente excepcional", "muy fácil de usar",
    "la mejor inversión que he hecho", "increíblemente rápido y eficiente", "diseño hermoso y funcional",
    "perfectamente integrado", "excelente relación calidad-precio", "muy satisfecho con la compra",
    "funciona de maravilla", "absolutamente fantástico", "lo recomiendo al 100%", "no puedo estar más feliz",
    "exactamente lo que necesitaba", "producto innovador y útil", "simplificó mi trabajo diario",
    "calidad premium", "me ahorra mucho tiempo", "interfaz intuitiva y amigable",
    "actualizaciones constantes y útiles", "soporte técnico muy profesional", "vale cada centavo",
    "rendimiento excepcional", "fácil configuración", "muy confiable", "supera a la competencia",
    "producto bien pensado", "me encanta cada detalle", "muy recomendable", "funciona sin problemas",
    "gran innovación", "servicio impecable", "la mejor web", "increíble servicio", "excelente trabajo",
    "muy buena calidad", "estoy muy contento", "magnífico producto", "realmente impresionante",
    "la mejor opción", "sobresaliente", "altamente recomendado", "perfecto para mis necesidades",
    "excepcional calidad", "brillante implementación", "fantástica experiencia", "maravilloso servicio",
    "extraordinario producto", "genial en todo sentido", "impecable atención", "espectacular resultado",
    "lo mejor que he probado", "inmejorable calidad", "excelente en todos los aspectos", "notable mejora",
    "admirable trabajo", "superior a todo", "destacable producto", "sorprendentemente bueno",
    "realmente satisfactorio", "muy impresionado", "la mejor experiencia", "extraordinariamente bueno",
    "excepcional en todo", "verdaderamente excelente", "incomparable calidad", "magnífica solución",
    "extremadamente satisfecho", "fantástico en general", "muy bien diseñado", "perfecta ejecución",
    "brillante idea", "asombroso resultado", "formidable producto", "estupendo servicio",
    "exquisito trabajo", "soberbio rendimiento", "espléndido diseño", "admirable atención",
    "me encanta", "súper bueno", "de lo mejor", "cinco estrellas", "amor total",
    "perfecto", "ideal", "maravilloso", "excelente", "genial", "fantástico", "increíble",
    "espectacular", "extraordinario", "brillante", "magnífico", "estupendo", "formidable",
]

negativos = [
    "la aplicación tiene muchos errores", "el diseño de la interfaz es confuso",
    "la documentación no es clara", "el rendimiento es lento", "no pude completar mi tarea",
    "el sistema se cae constantemente", "no entiendo cómo usar esta funcionalidad",
    "la actualización introdujo más errores", "la funcionalidad prometida no está disponible",
    "consume demasiados recursos", "no puedo acceder a mi cuenta", "tiempos de carga largos",
    "el sistema no guarda mis cambios", "el soporte no responde a tiempo",
    "no es compatible con mi dispositivo", "muy decepcionante", "pérdida total de dinero",
    "no funciona como prometieron", "pésima experiencia", "lleno de bugs",
    "nunca lo compraría de nuevo", "totalmente inútil", "complicado de usar", "mal diseño",
    "se congela constantemente", "no vale la pena", "terrible servicio al cliente",
    "muy frustrante", "no lo recomiendo", "problemas constantes", "difícil de configurar",
    "interfaz anticuada", "muy caro para lo que ofrece", "funciona mal",
    "no cumple las expectativas", "demasiados errores", "perdí información importante",
    "soporte técnico inútil", "lento e ineficiente", "muy deficiente", "no es intuitivo",
    "mala calidad", "no sirve para nada", "completamente inutilizable", "demasiado complicado",
    "experiencia horrible", "no volvería a comprarlo", "peor compra que he hecho",
    "totalmente defectuoso", "servicio deplorable", "la peor web", "horrible servicio",
    "pésimo trabajo", "muy mala calidad", "estoy muy decepcionado", "terrible producto",
    "realmente malo", "la peor opción", "deficiente en todo", "nada recomendable",
    "pésima implementación", "desastrosa experiencia", "pésimo servicio", "horrible producto",
    "malo en todo sentido", "terrible atención", "desastroso resultado", "lo peor que he probado",
    "pésima calidad", "malo en todos los aspectos", "terrible experiencia", "pésimo trabajo",
    "inferior a todo", "muy mal producto", "extremadamente malo", "muy insatisfecho",
    "terriblemente malo", "horriblemente diseñado", "pésima ejecución", "mala idea",
    "horrible resultado", "terrible en general", "muy mal hecho", "pésimo diseño",
    "terrible rendimiento", "no funciona", "me arrepiento", "no lo compren", "muy malo",
    "horrible", "pésimo", "terrible", "desastre", "decepción", "basura", "defectuoso",
    "inservible", "problemático", "deficiente", "inadecuado", "insatisfactorio",
]

neutrales = [
    "el producto llegó en la fecha indicada", "la instalación tomó 30 minutos",
    "está disponible en varios colores", "el manual incluye instrucciones básicas",
    "el producto mide 15x20 centímetros", "viene con garantía de un año",
    "compatible con Windows y Mac", "el empaque es estándar", "incluye cable USB",
    "requiere actualización periódica", "está hecho de plástico", "funciona con batería AA",
    "peso aproximado de 500 gramos", "disponible en tienda física", "puede verse en la página oficial",
    "existe versión gratuita", "requiere registro previo", "el precio es de $50 dólares",
    "funciona de forma básica", "cumple su función principal", "es similar a otros productos",
    "tiene opciones configurables", "la marca es conocida", "está en el mercado desde 2020",
    "versión actual es la 2.0", "requiere conexión a internet", "ocupa 500MB de espacio",
    "compatible con versiones anteriores", "incluye tutorial básico", "actualizado mensualmente",
    "disponible en varios idiomas", "el embalaje es reciclable", "cuenta con modo offline",
    "la interfaz tiene modo oscuro", "incluye soporte por email", "funciona según especificaciones",
    "diseño estándar del mercado", "características similares a versión anterior",
    "disponible para descarga directa", "proceso de compra normal", "tiene versión móvil",
    "la entrega fue puntual", "empaque sin daños", "producto tal como se describe",
    "cumple con lo básico", "ni bueno ni malo", "es lo que esperaba", "sin sorpresas",
    "producto común", "normal para el precio", "viene en caja", "incluye manual",
    "fabricado en China", "color negro", "tamaño mediano", "peso ligero", "material estándar",
    "funciona con electricidad", "tiene botones", "pantalla LCD", "conexión por cable",
    "incluye pilas", "diseño rectangular", "acabado mate", "viene sellado", "formato digital",
    "duración estimada", "capacidad de 1GB", "resolución HD", "frecuencia 50Hz",
    "temperatura ambiente", "uso doméstico", "instalación sencilla", "mantenimiento anual",
    "garantía limitada", "stock disponible", "envío incluido", "pago contra entrega",
    "diferentes modelos", "varias tallas", "distintas versiones", "múltiples opciones",
    "fabricante reconocido", "distribuidor oficial", "importado", "nacional", "genérico",
]

min_length = min(len(positivos), len(negativos), len(neutrales))
texts = positivos[:min_length] + negativos[:min_length] + neutrales[:min_length]
labels = (["positivo"] * min_length + ["negativo"] * min_length + ["neutral"] * min_length)

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42, stratify=labels
)

pipeline = Pipeline([
    ("vect", TfidfVectorizer(
        max_features=1000,
        ngram_range=(1, 3),
        min_df=1,
        sublinear_tf=True,
        strip_accents='unicode'
    )),
    ("clf", LogisticRegression(
        C=10.0,
        max_iter=1000,
        random_state=42,
        class_weight='balanced'
    ))
])

pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

test_phrases = [
    "la mejor web",
    "excelente página",
    "me encanta",
    "muy malo",
    "terrible servicio",
    "no funciona",
    "el producto mide 20cm",
    "está disponible",
    "color azul"
]

for phrase in test_phrases:
    pred = pipeline.predict([phrase])[0]
    probs = pipeline.predict_proba([phrase])[0]
    classes = pipeline.classes_
    prob_dict = {cls: f"{prob*100:.1f}%" for cls, prob in zip(classes, probs)}

dump(pipeline, "sentiment_model.joblib")
