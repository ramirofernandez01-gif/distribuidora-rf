document.addEventListener('DOMContentLoaded', function() {
    
    const logoElement = document.getElementById('logo');
    
    anime({
        targets: logoElement,
        scale: [0, 1],
        opacity: [0, 1],
        rotate: [720, 0],
        duration: 2000,
        easing: 'easeOutElastic(1, .8)',
    });

    function initMap() {
        const location = { lat: -34.6037, lng: -58.3816 };
        const map = new google.maps.Map(document.getElementById("map"), {
            zoom: 12,
            center: location,
        });
        const marker = new google.maps.Marker({
            position: location,
            map: map,
            title: "Nuestra Ubicación",
        });
    }
    window.initMap = initMap;

    initMap();

});
