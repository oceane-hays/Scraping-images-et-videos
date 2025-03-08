import sys
import requests
import re


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

url = args[-1]

response = requests.get(url)


while True :
    if url[-1] == "/" :
        break
    url = url[:-1]


path = "PATH "

doc = ''.join(response.text.split('    '))
doc = doc.replace("\t", "")
doc = doc.replace(">", " ")
doc = ''.join(doc.split('\n'))
doc = doc.split('<')

def estVideo(x) :
    return "video" in x or "source" in x

def filtrer(doc):
    return list(filter(lambda x: "img" in x or estVideo(x), doc))


doc = filtrer(doc)

image = "IMAGE "
video = "VIDEO "

resultat = []

for i in range(len(doc)) :

    ligne = re.findall(r'[^"\s]+="[^"]*"|[^"\s]+', doc[i])

    if ligne[0] == "img" :
        for j in range(len(ligne)) :
            if "src" in ligne[j] :
                image += ligne[j][5:-1]

            if "alt" in ligne[j] :
                image += " " + ligne[j][4:]
        resultat.append(image)
        image = "IMAGE "

    if ligne[0] == "video":
        for j in range(len(ligne)):
            if "src" in ligne[j]:
                video += ligne[j][5:-1]
                resultat.append(video)
                video = "VIDEO "

    if ligne[0] == "source":
        for j in range(len(ligne)):
            if "src" in ligne[j]:
                video += ligne[j][5:-1]
                resultat.append(video)
                video = "VIDEO "



def define_options(args, res):
    global path
    global url

    i = 0
    while i < len(args):
        match args[i]:
            case "-r":

                if i + 1 < len(args) and args[i + 1] != url:
                    regex = args[i + 1]

                    res = filter(lambda x: regex in x, res)
                    i += 1
                else:
                    res = ["Erreur : -r requiert une valeur"]

            case "-i":
                res = filter(lambda x: x[0] != "I", res)

            case "-v":
                res = filter(lambda x: x[0] != "V", res)

            case "-p":
                if i + 1 < len(args) and args[i + 1] != url:
                    path += args[i + 1]
                    print(path)

                    temp = []
                    for line in res :
                        ligne = line.split()

                        ligne[1] = ligne[1].split("/")[-1]
                        temp.append(" ".join(ligne))

                    res = temp
                    i += 1

                else:
                    res = ["Erreur : -p requiert une valeur"]

            case "-h":
                print("----- HELP : Extracteur de video et d'images -----")
                for arg in range(len(args) - 1) :
                    print(args[arg], aide_arg[args[arg]])

        i += 1


    if path == "PATH " :
        print(path + url)
    return "\n".join(res)



if len(args) > 1 :
    print(define_options(args, resultat))

else :
    print(path + url)
    print("\n".join(resultat))
