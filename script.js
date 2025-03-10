// Function to show the popup when the mouse is pressed down
function showPopup(imgSrc) {
    let popup = document.getElementById("imagePopup");
    let popupImg = document.getElementById("popupImg");

    popupImg.src = imgSrc;
    popup.style.display = "block";
}

// Function to hide the popup when the mouse is released
function hidePopup() {
    let popup = document.getElementById("imagePopup");
    popup.style.display = "none";
}

// Carousel & Gallery functionality
var images = {image_list};
var captions = {caption_list};
var index = 0;

function showTable() {
    document.getElementById("tableView").style.display = "block";
    document.getElementById("carousel").style.display = "none";
    document.getElementById("gallery").style.display = "none";
}

function showCarousel() {
    if (images.length === 0) return;
    document.getElementById("tableView").style.display = "none";
    document.getElementById("gallery").style.display = "none";
    document.getElementById("carousel").style.display = "block";
    updateCarousel();
}

function showGallery() {
    document.getElementById("tableView").style.display = "none";
    document.getElementById("carousel").style.display = "none";
    document.getElementById("gallery").style.display = "block";
}

function nextImage() {
    index = (index + 1) % images.length;
    updateCarousel();
}

function updateCarousel() {
    document.getElementById("carouselImage").src = images[index];
    document.getElementById("imageCaption").innerText = captions[index];

    // Update dots
    var dotsContainer = document.getElementById("dotsContainer");
    dotsContainer.innerHTML = "";
    for (var i = 0; i < images.length; i++) {
        var dot = document.createElement("span");
        dot.classList.add("dot");
        if (i === index) dot.classList.add("active-dot");
        dot.setAttribute("onclick", "setImage(" + i + ")");
        dotsContainer.appendChild(dot);
    }
}

function setImage(i) {
    index = i;
    updateCarousel();
}