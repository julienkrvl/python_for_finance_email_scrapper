# On importe les librairie
from urllib3 import ProxyManager, make_headers, PoolManager
import re
import csv
import random
import json
import sys

usernames = []
usernames_source_file = 'test.csv'
infos = []
proxys_source_file = 'proxys.csv'
proxy_list = []
dest_file = 'result.csv'

print("Importation des usernames en cours")

with open(usernames_source_file) as f:
    usernames = [s for line in f.readlines() for s in line[:-1].split(',')]

print("Importation OK")

print("Importation des proxys en cours")

with open(proxys_source_file) as f:
    proxy_list = [s for line in f.readlines() for s in line[:-1].split(',')]

print(proxy_list)
print("Importation OK")

index = 0
for username in usernames:
    index += 1
    # On fait la requete
    req = 'https://www.instagram.com/' + username + '/?__a=1'

    if len(proxy_list) >= 1:
        # On choisi le proxy au hasard
        proxy_number = random.randint(0, len(proxy_list) - 1)
        http = ProxyManager("http://" + proxy_list[proxy_number] + "/")
    else:
        http = PoolManager()

    webpage = http.request('GET', req)

    try:
        test = json.loads(webpage.data)
        webpage = str(webpage.data)
    except Exception as e:
        if len(proxy_list) >= 1:
            print("Ce proxy est cramé : " + proxy_list[proxy_number])
            proxy_list.remove(proxy_list[proxy_number])
        if len(proxy_list) < 1:
            print("Il n'y a plus de proxy disponible")
            with open(dest_file, "w") as output:
                writer = csv.writer(output, lineterminator='\n')
                for val in infos:
                    writer.writerow([val])

            print("Le fichier " + dest_file + "a bien été créé")
            sys.exit()
        continue

    emails = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", webpage)

    progression = (index / len(usernames)) * 100
    print("En cours : " + str(progression) + "%")

    try:
        infos.append(emails[0] + ", " + username)
    except:
        continue


with open(dest_file, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for val in infos:
        writer.writerow([val])

print("Le fichier " + dest_file + "a bien été créé")
