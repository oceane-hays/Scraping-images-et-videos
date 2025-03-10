document.addEventListener("DOMContentLoaded", function () {
    var table = document.getElementById("resourceTable");
    var popup = document.getElementById("imagePopup");
    var popupImage = document.getElementById("popupImage");

    // Handle table row clicks
    table.addEventListener("mousedown", function (event) {
        var row = event.target.closest("tr");
        if (row && row.dataset.src) {
            popupImage.src = row.dataset.src;
            popup.style.display = "block";
        }
    });

    // Hide popup when releasing mouse
    document.addEventListener("mouseup", function () {
        popup.style.display = "none";
    });

    // Handle button clicks (Gallery & Carousel)
    document.getElementById("showGallery").addEventListener("click", showGallery);
    document.getElementById("showCarousel").addEventListener("click", showCarousel);
});

function showGallery() {
   
}

function showCarousel() {
    
}

function updateCarousel() {
    
}