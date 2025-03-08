import shlex
import sys

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visualisation des Ressources</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; }}
        table {{ width: 80%; margin: auto; border-collapse: collapse; }}
        th, td {{ border: 1px solid black; padding: 10px; text-align: left; }}
        th {{ background-color: #007bff; color: white; }}

        /* Striped table */
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #ddd; }}

        .container {{ display: none; margin-top: 20px; }}
        .gallery img {{ width: 100px; height: auto; margin: 5px; }}

        /* Carousel Styling */
        .carousel {{ position: relative; display: flex; flex-direction: column; align-items: center; }}
        .carousel img {{ width: 50%; height: auto; border-radius: 10px; cursor: pointer; }}
        .caption {{ position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); 
                    background: rgba(0, 0, 0, 0.6); color: white; padding: 10px; border-radius: 5px; }}
        .dots {{ display: flex; justify-content: center; margin-top: 10px; }}
        .dot {{ height: 10px; width: 10px; margin: 0 5px; background-color: #bbb; 
                border-radius: 50%; display: inline-block; cursor: pointer; }}
        .active-dot {{ background-color: #007bff; }}

        /* Button Styling */
        button {{
            background-color: #007bff;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            margin: 10px;
        }}

        button:hover {{
            background-color: #0056b3;
        }}
    </style>
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

    <script>
        var images = {image_list};
        var captions = {caption_list};
        var index = 0;

        function showTable() {{
            document.getElementById("tableView").style.display = "block";
            document.getElementById("carousel").style.display = "none";
            document.getElementById("gallery").style.display = "none";
        }}

        function showCarousel() {{
            if (images.length === 0) return;
            document.getElementById("tableView").style.display = "none";
            document.getElementById("gallery").style.display = "none";
            document.getElementById("carousel").style.display = "block";
            updateCarousel();
        }}

        function showGallery() {{
            document.getElementById("tableView").style.display = "none";
            document.getElementById("carousel").style.display = "none";
            document.getElementById("gallery").style.display = "block";
        }}

        function nextImage() {{
            index = (index + 1) % images.length;
            updateCarousel();
        }}

        function updateCarousel() {{
            document.getElementById("carouselImage").src = images[index];
            document.getElementById("imageCaption").innerText = captions[index];

            // Update dots
            var dotsContainer = document.getElementById("dotsContainer");
            dotsContainer.innerHTML = "";
            for (var i = 0; i < images.length; i++) {{
                var dot = document.createElement("span");
                dot.classList.add("dot");
                if (i === index) dot.classList.add("active-dot");
                dot.setAttribute("onclick", "setImage(" + i + ")");
                dotsContainer.appendChild(dot);
            }}
        }}

        function setImage(i) {{
            index = i;
            updateCarousel();
        }}
    </script>

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
    path = resources[0].split(" ")[1]

    # Generate table rows and gallery images
    for i in range(1, len(resources)):
        ligne = shlex.split(resources[i])

        if len(ligne) >= 2:
            img_path = path + ligne[1]
            image_list.append(f"'{img_path}'")
            
            alt_text = ligne[2] if len(ligne) >= 3 else "Client Image"
            caption_text = f"Ressource {i} - {alt_text}"
            caption_list.append(f"'{caption_text}'")

            table_rows += f"<tr><td>{img_path}</td><td>{alt_text}</td></tr>\n"
            gallery_images += f'<img src="{img_path}" alt="{alt_text}">\n'

    first_image = image_list[0] if image_list else ""

    # Generate HTML content
    html_content = HTML_TEMPLATE.format(
        table_rows=table_rows, 
        gallery_images=gallery_images, 
        image_list=f"[{', '.join(image_list)}]",
        caption_list=f"[{', '.join(caption_list)}]",
        first_image=first_image
    )

    # Write HTML content to file
    with open("mapage.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Page HTML générée: mapage.html")

# Read resources from stdin
resources = sys.stdin.read().strip().split("\n")

if not resources or resources == [""]:
    print("Aucune ressource trouvée.", file=sys.stderr)
    sys.exit(1)

generate_html(resources)