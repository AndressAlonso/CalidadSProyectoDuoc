function MostrarMensaje(mensaje) {
    var ElementoMensaje = document.createElement('div');
    ElementoMensaje.id = 'mensaje';
    ElementoMensaje.className = 'rounded-2 text-white bg-body position-fixed top-0 end-0 m-3';
    ElementoMensaje.innerHTML = `
        <span class="text-dark"></span>
    `;
    ElementoMensaje.querySelector('span').innerText = mensaje;
    document.body.appendChild(ElementoMensaje);
    
    setTimeout(function() {
        document.body.removeChild(ElementoMensaje);
    }, 4000);
}

window.onload = function() {
    var djangoMessages = document.querySelectorAll('#django-messages li');
    
    djangoMessages.forEach(function(item) {
        var message = item.getAttribute('data-message');
        var tags = item.getAttribute('data-tags');
        if (tags.includes('success') || tags.includes('error')) {
            MostrarMensaje(message);
        }
    });
}
