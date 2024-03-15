let cropper;
document.getElementById('imageInput').addEventListener('change', function(event) {
    var files = event.target.files;
    var imageContainer = document.getElementById('imageContainer');
    imageContainer.innerHTML = ''; // Clear the container

    if (files && files.length > 0) {
        var fileReader = new FileReader();
        
        fileReader.onload = function(e) {
            var newImage = document.createElement('img');
            newImage.setAttribute('src', e.target.result);
            imageContainer.appendChild(newImage);
            
            // Initialize CropperJS on this new image
            if (cropper) {
                cropper.destroy(); // Destroy the old cropper instance
            }
            cropper = new Cropper(newImage, {
                // CropperJS options here
                aspectRatio: 1 / 1,
                background: false,
                highlight: false,
                zoomable: false,
                zoomOnTouch: false,
                zoomOnWheel: false,

            });
        };

        fileReader.readAsDataURL(files[0]);
    }
});

document.getElementById('cropButton').addEventListener('click', function() {
    if (cropper) {
        var croppedCanvas = cropper.getCroppedCanvas();
        croppedCanvas.toBlob(function(blob) {
            eel.process_cropped_image(blob)();
        });
    }
});
