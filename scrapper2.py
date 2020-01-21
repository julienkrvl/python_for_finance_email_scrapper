# On importe les librairie
from urllib.request import Request, urlopen
import re
from bs4 import BeautifulSoup
import nltk
nltk.download('stopwords')

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

    # Je vous présente ici la 2éme solution

# Il suffit de faire une boucle for sur urls[] pour faire les requetes de tous les site web trouvé



# On print le nom de domaine
print(urls[12])
# On fait la requete
req = Request(urls[12], headers={'User-Agent': 'Mozilla/5.0'}) # Ici je ne prend que une valeur (urls[12] pour l'exmemple) pour ne pas faire des centaines de requetes.
# On lis le resulat de la requete
webpage = urlopen(req).read()
# On converti le resultat en UTF8
webpage = webpage.decode("utf8")
# On converti le text en html
soup = BeautifulSoup(webpage, "html5lib")
# On exlu tout le script qui est dans le html
[s.extract() for s in soup('script')]
# On extrait le text du html
text = soup.get_text()
# On extrait tout les mots dans ce text est on le met dans une liste
tokens = re.findall('\w+', text)

words = []
# On mets tous les mots en minuscule
for word in tokens:
    words.append(word.lower())
# On télécharge les stop words francais
sw = nltk.corpus.stopwords.words('french')

words_ns = []
# On enleve les stopwords de la liste
for word in words:
    if word not in sw:
        words_ns.append(word)
# On garde seulement les mots qui apparait plus de 7 fois
from collections import Counter
counts = Counter(words_ns)
dupwords_ns = [id for id in words_ns if counts[id] > 7]
# Puis on supprime les doublons pour que cela soit plus propre
dupwords_ns = list(dict.fromkeys(dupwords_ns))
# On print les mots clés
print(dupwords_ns)
# On extrait les emails
emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", webpage)
emails = list(dict.fromkeys(emails))
# On print les emails
print(emails)
