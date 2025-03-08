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
        th {{ background-color: #007bff; color: white; }} /* Blue header */
        
        /* Striped table */
        tr:nth-child(even) {{ background-color: #f2f2f2; }} /* Alternating row colors */
        tr:hover {{ background-color: #ddd; }} /* Hover effect */

        .container {{ display: none; margin-top: 20px; }}
        .gallery img {{ width: 100px; height: auto; margin: 5px; }}
        .carousel img {{ width: 50%; height: auto; }}

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
        <img id="carouselImage" src="" alt="">
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
        var index = 0;

        function showTable() {{
            document.getElementById("tableView").style.display = "block";
            document.getElementById("carousel").style.display = "none";
            document.getElementById("gallery").style.display = "none";
        }}

        function showCarousel() {{
            document.getElementById("tableView").style.display = "none";
            document.getElementById("gallery").style.display = "none";
            document.getElementById("carousel").style.display = "block";
            startCarousel();
        }}

        function showGallery() {{
            document.getElementById("tableView").style.display = "none";
            document.getElementById("carousel").style.display = "none";
            document.getElementById("gallery").style.display = "block";
        }}

        function startCarousel() {{
            var img = document.getElementById("carouselImage");
            img.src = images[index % images.length];
            index++;
            setTimeout(startCarousel, 2000);
        }}
    </script>

</body>
</html>
"""

def generate_html(resources):
    table_rows = ""
    gallery_images = ""
    image_list = []

    path = resources[0].split(" ")[1]
    print(path)

    for i in range(1, len(resources)):
        ligne = shlex.split(resources[i])
        print(ligne)
        image_list.append(f"'{resources[i]}'")  # Store images in JavaScript array

        if len(ligne) >= 3:
            table_rows += f"<tr><td>{resources[i]}</td><td>{ligne[2]}</td></tr>\n"
            gallery_images += f'<img src="{path + ligne[1]}" alt="{ligne[2]}">\n'
        else:
            table_rows += f"<tr><td>{resources[i]}</td><td>{""}</td></tr>\n"
            gallery_images += f'<img src="{path + ligne[1]}">\n'

    html_content = HTML_TEMPLATE.format(
        table_rows=table_rows, 
        gallery_images=gallery_images, 
        image_list=f"[{', '.join(image_list)}]"
    )

    with open("mapage.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Page HTML générée: mapage.html")

resources = sys.stdin.read().strip().split("\n")

print(resources)

if not resources or resources == [""]:
    print("Aucune ressource trouvée.", file=sys.stderr)
    sys.exit(1)

generate_html(resources)
