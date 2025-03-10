var images = [];
var captions = [];
var index = 0;

document.addEventListener("DOMContentLoaded", function () {
    images = JSON.parse(document.getElementById("imageData").textContent);
    captions = JSON.parse(document.getElementById("captionData").textContent);

    if (images.length > 0) {
        document.getElementById("carouselImage").src = images[0];
        document.getElementById("imageCaption").innerText = captions[0];
        updateDots();
    }

    document.querySelectorAll("tr").forEach(row => {
        row.addEventListener("mousedown", function () {
            let imgSrc = row.cells[0].innerText; // Get image URL from the first column
            showPopup(imgSrc);
        });

        row.addEventListener("mouseup", hidePopup);
        row.addEventListener("mouseleave", hidePopup); // Hide if mouse leaves the row
    });
});

function showPopup(imgSrc) {
    let popup = document.getElementById("imagePopup");
    let popupImg = document.getElementById("popupImg");

    popupImg.src = imgSrc;
    popup.style.display = "block";
}

function hidePopup() {
    let popup = document.getElementById("imagePopup");
    popup.style.display = "none";
}

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
    updateDots();
}

function updateDots() {
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