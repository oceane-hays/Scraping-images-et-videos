import shlex
import sys

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualisation des Ressources</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <h1>Visualisateur</h1>
    <h3>d’images/vidéo</h3>

    <!-- Table View -->
    <div id="tableView">
        <table>
            <thead>
                <tr>
                    <th>Ressource</th>
                    <th>Alt</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>

        <button onclick="showCarousel()">Carrousel</button>
        <button onclick="showGallery()">Galerie</button>
    </div>

    <!-- Carousel View -->
    <div id="carousel" class="container carousel">
        <div class="caption" id="imageCaption"></div>
        <img id="carouselImage" src="{first_image}" alt="Carrousel Image" onclick="nextImage()">
        <div class="dots" id="dotsContainer"></div>
        <br>
        <button onclick="showTable()">Back</button>
    </div>

    <!-- Gallery View -->
    <div id="gallery" class="container gallery">
        {gallery_images}
        <br>
        <button onclick="showTable()">Back</button>
    </div>

    <!-- Popup View -->
    <div id="imagePopup">
        <img id="popupImg" src="">
    </div>

    <!-- Hidden JSON Data for JavaScript -->
    <script id="imageData" type="application/json">{image_list}</script>
    <script id="captionData" type="application/json">{caption_list}</script>
    <script src="script.js"></script>
</body>
</html>
"""

def generate_html(resources):
    table_rows = ""
    gallery_images = ""
    image_list = []
    caption_list = []

    if not resources or len(resources) < 2:
        print("Aucune ressource trouvée.", file=sys.stderr)
        sys.exit(1)

    # Extract base path
    path = ""
    if resources[0].startswith("PATH"):
        path = resources[0].split(" ", 1)[1] 

    for i in range(1, len(resources)):
        ligne = shlex.split(resources[i])  

        if len(ligne) >= 2 and ligne[0] == "IMAGE":
            img_path = ligne[1]  

            # Store in lists for script.js
            image_list.append(f'"{img_path}"')
            alt_text = ligne[2] if len(ligne) >= 3 else "Client Image"
            caption_list.append(f'"{alt_text}"')

            table_rows += f'<tr onmousedown="showPopup(\'{img_path}\')" onmouseup="hidePopup()">'
            table_rows += f'<td>{img_path}</td><td>{alt_text}</td></tr>\n'  

            gallery_images += f'<img src="{img_path}" alt="{alt_text}">\n'

    first_image = image_list[0] if image_list else ""

    html_content = HTML_TEMPLATE.format(
        table_rows=table_rows,
        gallery_images=gallery_images,
        image_list=f"[{', '.join(image_list)}]",
        caption_list=f"[{', '.join(caption_list)}]",
        first_image=first_image
    )

    with open("mapage.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Page HTML générée: mapage.html")

resources = sys.stdin.read().strip().split("\n")

generate_html(resources)