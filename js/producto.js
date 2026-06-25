document.addEventListener('DOMContentLoaded', function() {
    console.log('🎮 Script producto.js cargado correctamente');
    
    initializeProductCards();
    setupImageHandling();
});

function initializeProductCards() {
    const productCards = document.querySelectorAll('.flip-card');
    
    productCards.forEach(card => {
        setupFlipCardEvents(card);
        setupImageLoader(card);
    });
    
    console.log(`✅ Inicializadas ${productCards.length} cards de producto`);
}

function setupFlipCardEvents(card) {
    let isFlipped = false;
    
    card.addEventListener('click', function(e) {
        if (e.target.closest('button') || e.target.closest('a')) {
            return;
        }
        
        isFlipped = !isFlipped;
        card.classList.toggle('flipped', isFlipped);
        
        const flipIcon = card.querySelector('.flip-icon');
        if (flipIcon) {
            flipIcon.style.transform = isFlipped ? 'rotate(180deg)' : 'rotate(0deg)';
        }
        
        console.log(`🔄 Card ${card.dataset.productoId || 'sin-id'} ${isFlipped ? 'volteada' : 'normal'}`);
    });
    
    card.addEventListener('mouseenter', function() {
        card.style.transform = 'translateY(-5px)';
        card.style.boxShadow = '0 20px 40px rgba(0,0,0,0.1)';
    });
    
    card.addEventListener('mouseleave', function() {
        card.style.transform = 'translateY(0)';
        card.style.boxShadow = '0 10px 30px rgba(0,0,0,0.08)';
    });
}

function setupImageLoader(card) {
    const img = card.querySelector('.producto-image');
    const placeholder = card.querySelector('.placeholder-content');
    
    if (!img || !placeholder) return;
    
    img.addEventListener('load', function() {
        placeholder.style.display = 'none';
        img.style.display = 'block';
        img.classList.add('fade-in');
        
        console.log(`🖼️ Imagen cargada para producto ${card.dataset.productoId || 'sin-id'}`);
    });
    
    img.addEventListener('error', function() {
        placeholder.style.display = 'block';
        img.style.display = 'none';
        
        console.log(`❌ Error cargando imagen para producto ${card.dataset.productoId || 'sin-id'}`);
    });
}

function setupImageHandling() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

function addToCart(productoId, button) {
    event.stopPropagation();
    
    const card = button.closest('.flip-card');
    const name = card.querySelector('h3').innerText;
    let priceText = card.querySelector('.absolute.bottom-3.right-3 span').innerText;
    const price = parseFloat(priceText.replace('$', '').replace(/\\./g, '').replace(',', '.'));
    const img = card.querySelector('.producto-image');
    const imageSrc = img ? img.src : '';
    
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    let existingItem = cart.find(item => item.id === productoId);
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: productoId,
            name: name,
            price: price,
            image: imageSrc,
            quantity: 1
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    
    if (typeof updateCartBadge === 'function') {
        updateCartBadge();
    }
    
    const originalText = button.innerHTML;
    
    button.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Agregando...
    `;
    
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = `
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
            ¡Agregado!
        `;
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 2000);
        
        console.log(`🛒 Producto ${productoId} agregado al carrito`);
    }, 1000);
}

const additionalStyles = `
<style>
    .fade-in {
        animation: fadeInImage 0.5s ease-in;
    }
    
    @keyframes fadeInImage {
        from { opacity: 0; transform: scale(1.1); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .flip-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .flip-card-inner {
        transition: transform 0.8s cubic-bezier(0.4, 0.0, 0.2, 1);
    }
    
    .flip-icon {
        transition: transform 0.3s ease;
    }
    
    .add-to-cart-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .add-to-cart-btn:active {
        transform: translateY(0);
    }
    
    .placeholder-content {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
</style>
`;

document.head.insertAdjacentHTML('beforeend', additionalStyles);

window.addToCart = addToCart;

console.log('🎯 Funcionalidad completa de producto.js cargada');