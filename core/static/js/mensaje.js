function MostrarMensaje(mensaje) {
    var ElementoMensaje = document.createElement('div');
    ElementoMensaje.id = 'mensaje';
    ElementoMensaje.className = 'toast text-wrap align-items-center text-bg-success border-0 position-fixed top-0 end-0 mt-3 m-md-3';
    ElementoMensaje.setAttribute('role', 'alert');
    ElementoMensaje.setAttribute('aria-live', 'assertive');
    ElementoMensaje.setAttribute('aria-atomic', 'true');
    
    ElementoMensaje.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${mensaje}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    document.body.appendChild(ElementoMensaje);
    
    // Initialize the Bootstrap toast functionality
    var toast = new bootstrap.Toast(ElementoMensaje);
    toast.show();

    // Automatically remove the element after it is hidden
    ElementoMensaje.addEventListener('hidden.bs.toast', function () {
        document.body.removeChild(ElementoMensaje);
    });
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
