
  document.addEventListener('DOMContentLoaded', function() {
    var modificarProductoModal = document.getElementById('modificarProducto');

    modificarProductoModal.addEventListener('show.bs.modal', function(event) {
      var button = event.relatedTarget;
      var id = button.getAttribute('data-id');
      var nombre = button.getAttribute('data-nombre');
      var stock = button.getAttribute('data-stock');
      var precio = button.getAttribute('data-precio');
      var descripcion = button.getAttribute('data-descripcion');
      var tipo = button.getAttribute('data-tipo');
      var pagina = button.getAttribute('data-pagina');

      var modalNombre = modificarProductoModal.querySelector('#nombreProducto');
      var modalStock = modificarProductoModal.querySelector('#stock');
      var modalPrecio = modificarProductoModal.querySelector('input[name="precio"]');
      var modalDescripcion = modificarProductoModal.querySelector('#descP');
      var modalTipo = modificarProductoModal.querySelector('#tipoProducto');
      var modalId = modificarProductoModal.querySelector('#producto_id');  
      var paginaData = modificarProductoModal.querySelector('#paginaData');  

      modalId.value = id;
      modalNombre.value = nombre;
      modalStock.value = stock;
      modalPrecio.value = precio;
      modalDescripcion.value = descripcion;
      modalTipo.value = tipo;
      paginaData.value = pagina;
    });
  });

