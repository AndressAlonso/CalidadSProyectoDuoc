const imageInput = document.getElementById('imageInput');
const imageContainer = document.getElementById('imageContainer');

imageInput.addEventListener('change', function (event) {
    const file = event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            // Mostrar la imagen
            const img = document.createElement('img');
            img.src = e.target.result;
            img.classList.add('img-fluid'); // Clase de Bootstrap para hacer la imagen adaptable
          img.style.maxHeight = '200px';  // Altura máxima

            imageContainer.innerHTML = '';
            imageContainer.appendChild(img);

            console.log(e.target.result);
        };

        reader.readAsDataURL(file);
    } 
});