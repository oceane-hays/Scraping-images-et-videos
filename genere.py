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
                    <th>alt</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>

        <button onclick="showCarousel()">Carrousel</button>
        <button onclick="showGallery()">Galerie</button>
    </div>

    <!-- Carrousel View -->
    <div id="carousel" class="container carousel">
        <img id="carouselImage" src="{first_image}" alt="Carrousel Image" onclick="nextImage()">
        <div class="caption" id="imageCaption"></div>
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

    path = resources[0].split(" ")[1]

    for i in range(1, len(resources)):
        ligne = shlex.split(resources[i])

        if len(ligne) >= 2:
            img_path = path + ligne[1]
            image_list.append(f"'{img_path}'")
            alt_text = ligne[2] if len(ligne) >= 3 else "Client Image"
            caption_text = f"Ressource {i} - {alt_text}"
            caption_list.append(f"'{caption_text}'")

            # Show popup only while mouse is pressed
            table_rows += f'<tr onmousedown="showPopup(\'{img_path}\')" onmouseup="hidePopup()"><td>{img_path}</td><td>{alt_text}</td></tr>\n'

            gallery_images += f'<img src="{img_path}" alt="{alt_text}">\n'

    html_content = HTML_TEMPLATE.format(
        table_rows=table_rows, 
        gallery_images=gallery_images, 
        image_list=f"[{', '.join(image_list)}]",
        caption_list=f"[{', '.join(caption_list)}]",
        first_image=image_list[0] if image_list else ""
    )

    with open("mapage.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Page HTML générée: mapage.html")

resources = sys.stdin.read().strip().split("\n")

if not resources:
    print("Aucune ressource trouvée.", file=sys.stderr)
    sys.exit(1)

generate_html(resources)