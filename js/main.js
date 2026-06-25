document.addEventListener('DOMContentLoaded', function() {
    
    console.log('🧼 CleanSA - Sistema cargado');

    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('card-visible');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.card-left, .card-right, .card-up, .info-card').forEach(card => {
        observer.observe(card);
    });

    anime({
        targets: '#main-title',
        scale: [0.8, 1],
        opacity: [0, 1],
        duration: 1200,
        easing: 'easeOutElastic(1, .8)',
        delay: 200
    });

    anime({
        targets: '.nav-card:first-child',
        opacity: [0, 1],
        translateY: [-30, 0],
        duration: 1000,
        easing: 'easeOutCubic',
        delay: 400
    });

    anime({
        targets: '.modern-card',
        opacity: [0, 1],
        translateY: [50, 0],
        scale: [0.9, 1],
        duration: 800,
        delay: anime.stagger(300, {start: 600}),
        easing: 'easeOutCubic'
    });

    anime({
        targets: '.pulse-icon',
        scale: [1, 1.05, 1],
        duration: 2000,
        loop: true,
        easing: 'easeInOutSine'
    });

    const infoCards = document.querySelectorAll('.info-card');
    infoCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            anime({
                targets: card,
                translateY: -8,
                scale: 1.02,
                duration: 300,
                easing: 'easeOutCubic'
            });
        });
        
        card.addEventListener('mouseleave', () => {
            anime({
                targets: card,
                translateY: 0,
                scale: 1,
                duration: 300,
                easing: 'easeOutCubic'
            });
        });
    });

    const firstElement = document.getElementById('first');
    if (firstElement) {
        const text = firstElement.textContent;
        firstElement.innerHTML = '';
        
        for (let i = 0; i < text.length; i++) {
            const span = document.createElement('span');
            span.textContent = text[i] === ' ' ? '\u00A0' : text[i];
            span.style.display = 'inline-block';
            span.style.opacity = '0';
            firstElement.appendChild(span);
        }
        
        anime({
            targets: '#first span',
            opacity: [0, 1],
            y: [ { to: '-2.75rem', ease: 'outExpo', duration: 400 },
            { to: 0, ease: 'outBounce', duration: 300, delay: 100 },
            ],  
            rotateZ: [-180, 1],
            duration: 250,
            delay: anime.stagger(80),
            easing: 'easeOutElastic(1, .8)',
            loop: true,
            direction: 'alternate',
            loopDelay: 1000
        });
    }

    setTimeout(() => {
        console.log('✨ Animaciones CleanSA iniciadas');
    }, 1500);
});