import os
import shutil
import sys
from urllib.parse import urljoin

import requests
import re

# HELP
aide_arg = {
    "-r <regex>" : "    (@oceane-hays, @CelinaZhang11) liste seulement les ressources dont le nom  matche l’expression régulière.",
    "-i" : "    (@oceane-hays, @CelinaZhang11) ne liste pas les elements <img>.",
    "-v" : "    (@oceane-hays, @CelinaZhang11) ne liste pas les elements <video>.",
    "-p <path>" : "    (@oceane-hays, @CelinaZhang11) liste et copie es ressources img et/ou video de <url> dans le path.",
    "-h" : "    (@oceane-hays, @CelinaZhang11) affiche le synopsis de la commande et les auteurs de la commande",
}

args = sys.argv[1:]

if len(args) < 1:
    print("Usage: extract.py (synopsis) <url>")
    sys.exit(1)

url = args[-1].rstrip("/")

response = requests.get(url)
html = response.text

img_pattern = re.findall(r'<img[^>]+src=["\'](.*?)["\'].*?>', html, re.IGNORECASE)
video_pattern = re.findall(r'<video[^>]+src=["\'](.*?)["\'].*?>', html, re.IGNORECASE)
source_pattern = re.findall(r'<source[^>]+src=["\'](.*?)["\'].*?>', html, re.IGNORECASE)

def normalize_url(src, base_url):
    if src.startswith("//"):
        return "https:" + src
    return urljoin(base_url, src)

resultat = [f"IMAGE {normalize_url(src, url)}" for src in img_pattern] + \
           [f"VIDEO {normalize_url(src, url)}" for src in video_pattern + source_pattern]


path = "PATH "

def define_options(args, res):
    global url

    filtered_res = res

    i = 0
    while i < len(args):
        match args[i]:
            case "-r":
                if i + 1 < len(args) and args[i + 1] != url:
                    regex = args[i + 1]
                    filtered_res = [line for line in filtered_res if re.search(regex, line)]
                    i += 1

            case "-i":
                filtered_res = [line for line in filtered_res if not line.startswith("IMAGE")]

            case "-v":
                filtered_res = [line for line in filtered_res if not line.startswith("VIDEO")]

            case "-p":
                if i + 1 < len(args) and args[i + 1] != url and not args[i + 1].startswith("-"):
                    path = args[i + 1]
                    os.makedirs(path, exist_ok=True)

                    output_file = os.path.join(path, "extracted_resources.txt")
                    with open(output_file, "w") as file:
                        file.write("\n".join(filtered_res))

                    print(f"PATH {output_file}")
                    i += 1

            case "-h":
                print("----- HELP : Extracteur de vidéo et d'images -----")
                for option, desc in aide_arg.items():
                    print(f"{option} : {desc}")

        i += 1

    return "\n".join(filtered_res)


if "-p" not in args:
    print("PATH " + url)

if len(args) > 1:
    print(define_options(args, resultat))
else:
    print("\n".join(resultat))
