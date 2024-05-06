function loadPreview(event) {
    var image = document.getElementById('post_thumbnail');
    image.src = URL.createObjectURL(event.target.files[0]);
};