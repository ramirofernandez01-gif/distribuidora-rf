document.addEventListener('DOMContentLoaded', function() {
    anime({
        targets: shopElement,
        scale: [0.8, 1],
        opacity: [0, 1],
        duration: 1000,
        easing: 'easeOutQuart',
    });
});
