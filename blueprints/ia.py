from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from joblib import load

MODEL_PATH = "sentiment_model.joblib"
model = load(MODEL_PATH)

ia_bp = Blueprint('ia', __name__, url_prefix='/ia')


@ia_bp.route("/", methods=["GET"])
def ia():
    return render_template("ia.html")


@ia_bp.route("/predict", methods=["POST"])
def predict():
    text = request.form.get("text", "")
    if not text:
        return render_template("ia.html", error="Ingresá un texto para analizar.")
    pred = model.predict([text])[0]
    probs = model.predict_proba([text])[0]
    classes = model.classes_
    prob_dict = {cls: float(round(prob, 4)) for cls, prob in zip(classes, probs)}
    return render_template("ia.html", text=text, prediction=pred, probs=prob_dict)


@ia_bp.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "ok"})
