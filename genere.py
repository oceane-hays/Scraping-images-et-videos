import shlex
import sys

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualisation des Ressources</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>

    <h1>Visualisateur</h1>
    
    <div id="content">
        <table id="resourceTable">
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
    </div>

    <button id="showCarousel">Carrousel</button>
    <button id="showGallery">Galerie</button>

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

    <!-- Image Popup -->
    <div id="imagePopup">
        <img id="popupImage" src="" alt="Image Preview">
    </div>

    <script src="script.js"></script>

</body>
</html>
"""

def generate_html(resources):
    table_rows = ""

    if not resources or len(resources) < 2:
        print("Aucune ressource trouvée.", file=sys.stderr)
        sys.exit(1)

    # Extract base path
    path = resources[0].split(" ")[1]

    # Generate table rows with data attributes
    for i in range(1, len(resources)):
        ligne = shlex.split(resources[i])

        if len(ligne) >= 2:
            img_path = path + ligne[1]
            alt_text = ligne[2] if len(ligne) >= 3 else "Client Image"

            table_rows += f'<tr data-src="{img_path}"><td>{img_path}</td><td>{alt_text}</td></tr>\n'

    # Generate HTML content
    html_content = HTML_TEMPLATE.format(table_rows=table_rows)

    # Write to file
    with open("mapage.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Page HTML générée: mapage.html")

# Read resources from stdin
resources = sys.stdin.read().strip().split("\n")

if not resources or resources == [""]:
    print("Aucune ressource trouvée.", file=sys.stderr)
    sys.exit(1)

generate_html(resources)