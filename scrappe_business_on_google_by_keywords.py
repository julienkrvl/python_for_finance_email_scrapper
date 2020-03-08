# On importe les librairies
from urllib3 import ProxyManager, make_headers, PoolManager
import re
import time
import random
import csv

# On définie les mots clés de la requete
keyword1 = "boutique en ligne"
keyword2 = "lingerie"
keyword3 = "contact"

sleep_time = 5
min_url_per_page = 20

# AUTORISER LES PROXY sur https://instantproxies.com/ avant d'utiliser le script
proxy_list = ["104.140.164.203:3128", "192.126.164.82:3128", "173.234.181.40:3128", "173.234.181.138:3128", "192.126.164.228:3128", "173.234.181.222:3128", "192.126.153.6:3128", "104.140.164.245:3128", "173.234.181.197:3128", "192.126.153.129:3128"]

urls_full = []
emails_full = []

for page in range(0, 10):
    # On fait la requete
    start = page * 100
    req = 'https://www.google.com/search?q=%22' + keyword1 + '%22+%22' + keyword2 + '%22+%22' + keyword3 + '%22' + '%22&num=100&start=' + str(start)
    # On choisi le proxy au hasard
    proxy_number = random.randint(0, len(proxy_list) - 1)
    http = ProxyManager("http://" + proxy_list[proxy_number] + "/")
    # http = PoolManager() # Si on utilise pas de proxy
    # On lis le resulat de la requete
    webpage = http.request('GET', req)
    # On verifie si le proxy n'est pas cramé
    if webpage.status == 403:
        print("Ce proxy est cramé : " + proxy_list[proxy_number])
        proxy_list.remove(proxy_list[proxy_number])
        continue
    elif webpage.status == 429:
        print("Ce proxy demande un capcha : " + proxy_list[proxy_number])
        proxy_list.remove(proxy_list[proxy_number])
        continue
    if len(proxy_list) < 1:
        print("Il n'y a plus de proxy disponible")
        sys.exit()
    # On converti le resultat en texte
    webpage = str(webpage.data)
    # On récupere tout les urls qui se trouvent dans la reponse
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', webpage)
    urls_full.extend(urls)
    time.sleep(sleep_time)
    print("Nombre d'urls pour la page " + str(page) + " : " + str(len(urls)))
    print("Nombre d'urls total : " + str(len(urls_full)))
    if len(urls) < min_url_per_page:
        print("break")
        break

# On enleve tous les urls du moteur de recherche : ici google
urls = [ x for x in urls if "google" not in x ]
urls_full = list(dict.fromkeys(urls_full))

for url in urls_full:
    # On choisi le proxy au hasard
    proxy_number = random.randint(0, len(proxy_list) - 1)
    http = ProxyManager("http://" + proxy_list[proxy_number] + "/")
    # http = PoolManager() # Si on utilise pas de proxy
    try:
        # On lis le resulat de la requete
        webpage = http.request('GET', url)
        # On converti le resultat en texte
        webpage = str(webpage.data)
    except:
        print("An exception occurred")
        continue
    # On cherche les emails
    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", webpage)
    emails_full.extend(emails)
    print("Nombre total d'emails trouvé : " + str(len(emails_full)))
    print(emails)




emails_full = list(dict.fromkeys(emails_full))

csvfile = "emails.csv"
#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in emails_full:
        writer.writerow([val])

print("Script OK") # Allez verifier le fichier emails.csv
