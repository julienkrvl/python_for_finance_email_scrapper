# On importe les librairie
from urllib3 import ProxyManager, make_headers, PoolManager
import re
import time
import random
import csv

#On définie les mots clés de la requete
networks = ["instagram.com", "facebook.com", "twitter.com"]
mails_providers = ["gmail.com", "hotmail.com", "hotmail.fr", "yahoo.com", "yahoo.fr", "live.fr"]
keyword = "voyage"
sleep_time = 5
min_email_per_page = 3

# AUTORISER LES PROXY sur https://instantproxies.com/ avant d'utiliser le script
proxy_list = ["104.140.164.203:3128", "192.126.164.82:3128", "173.234.181.40:3128", "173.234.181.138:3128", "192.126.164.228:3128", "173.234.181.222:3128", "192.126.153.6:3128", "104.140.164.245:3128", "173.234.181.197:3128", "192.126.153.129:3128"]

emails_full = []

for network in networks:
    for mail_provider in mails_providers:
        for page in range(0, 10):
            # On fait la requete
            start = page * 100
            req = 'https://www.google.com/search?q=site%3A' + network + '+%22' + keyword + '%22+%22%40' + mail_provider + '%22&num=100&start=' + str(start)
            # On choisi le proxy au hasard
            proxy_number = random.randint(0, 9)
            http = ProxyManager("http://" + proxy_list[proxy_number] + "/")
            # http = PoolManager() # Si on utilise pas de proxy
            # On lis le resulat de la requete
            webpage = http.request('GET', req)
            # On converti le resultat en texte
            webpage = str(webpage.data)
            # On cherche les emails
            emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", webpage)
            emails_full.extend(emails)
            time.sleep(sleep_time)
            print("Network : " + network + " Mail : " + mail_provider + " Page : " + str(page) + " Nombre resulat : " + str(len(emails)) )
            print("Nombre d'emails total : " + str(len(emails_full)))
            if len(emails) < min_email_per_page:
                print("break")
                break


emails_full = list(dict.fromkeys(emails_full))

csvfile = "emails.csv"
#Assuming res is a flat list
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in emails_full:
        writer.writerow([val])

print(emails_full)
