# Ce scrapper utilise une API externe (hunter.io)
# Voir scrapper2.py pour utiliser ce scrapper sans API

# On importe les librairie
from urllib.request import Request, urlopen
import re
from pyhunter import PyHunter
hunter = PyHunter('') # Clés API privée sparkpost

#On définie les mots clés de la requete
keyword1 = "boutique+en+ligne"
keyword2 = "lingerie"
keyword3 = "contact"

# On fait la requete
req = Request('https://www.google.fr/search?q=%22"' + keyword1 + '"%22+%22' + keyword2 + '%22+%22' + keyword3 + '%22&num=100', headers={'User-Agent': 'Mozilla/5.0'})
# On lis le resulat de la requete
webpage = urlopen(req).read()
# On converti le resultat en UTF8
webpage = webpage.decode("utf8")
# On récupere tout les urls qui se trouvent dans la reponse
urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', webpage)
# On enleve tous les urls du moteur de recherche : ici google
urls = [ x for x in urls if "google" not in x ]
# On supprime les doublons
urls = list(dict.fromkeys(urls))

# Ici j'ai eu le choix entre 2 strategies.
    # 1er solution : Utiliser Hunter.io | Problème : C'est trop chère pour un étudiant
    # 2eme solution : Trouvez les emails moi-même à l'aide de des nom de domaine | Problème : C'est galére et les adresses emails scrapper ne sont pas forcément les bonnes

    # je vous presente ici la 1er solution mais je ne ferais que une requete car c'est juste un petit projet (Je suis limité à 50 requete par mois en gratuit, sinon il faut payer).

domaineInformation = hunter.domain_search(urls[0]) # Je prend seulement le premier resulat, si on voudrait obtenir tous les informations il suffirait de faire une boucle for sur ces informations et de les enregistrer

print("Voici les informations obtenue :")
# ICI ON PEUT FAIRE LA BOUCLE
print("Pour le nom de domaine : " + domaineInformation["domain"])
print("Voici la liste des adresses emails :")
for info in domaineInformation["emails"]:
    print("Adresse email : " + info["value"]) # + " " + info["first_name"] + " " + info["last_name"] + " Role : " + info["position"] + " Tél : " + info["phone_number"] + "Linkedin : " + info["linkedin"])

information = hunter.account_information()
print("Il reste " + str(information["calls"]["left"]) + " requetes à l'API hunter.io sur le compte. " + "Le compte hunter.io appartient à " + information["first_name"] + " " + information["last_name"] + ", vous pouvez le contacter à " + information["email"])
