# Idée: faire la somme de tous les routeurs pour une même heure,
# et mettre une sorte de slider pour aller à d'autres heures (= moyennes)
# Et mettre la possibilité d'une moyenne globale

import os
import json
import requests
import folium

from dotenv import load_dotenv

# Charge les variables depuis le fichier .env
load_dotenv()
TOKEN = os.getenv("IPINFO_TOKEN")

if not TOKEN:
    raise SystemExit("Error: IPINFO_TOKEN not defined.")

REPORTS_FILE_NAME = "reports.json"

ROUTERS_POSITION_FILE_NAME = "routers_pos.json"

PARAMS = {"token": TOKEN}
def get_all_routers_pos(routers):
    for ip in routers:
        # Get more in-depth info on those IP addresses
        url = f"https://ipinfo.io/{ip}"
        #response = requests.get(url, PARAMS)
        response = requests.get(url)

        if response.status_code == 200:
            if "loc" in response.json():
            # On utilise le champ 'ip' de la réponse pour être sûr qu'on parle de la bonne adresse ip
                ip = response.json()["ip"]

                lat, long = response.json()["loc"].split(",")
                routers[ip]["lat"] = float(lat)
                routers[ip]["long"] = float(long)
        else:
            print(f"Error at IP {ip}: {response.status_code}")

    # Sauvegarde la position des routeurs dans un JSON
    with open(ROUTERS_POSITION_FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(routers, f, ensure_ascii=False, indent=4)

def create_map_from_routers_pos(jsonFile):
    with open(jsonFile, "r", encoding="utf-8") as f:
        data = json.load(f)

        first_key = next(iter(data))

        # Création de la carte
        m = folium.Map(location=[data[first_key]["lat"], data[first_key]["long"]], zoom_start=5)

        last_ip = None

        for ip in data:
            lat, long = data[ip]["lat"], data[ip]["long"]
            data[ip]["lat"] = float(lat)
            data[ip]["long"] = float(long)

            folium.CircleMarker(
                location = [data[ip]["lat"], data[ip]["long"]],
                radius=data[ip]["nb_times_encountered"],
                color = "red",
                fill = True,
                fill_color = "red",
                fill_opacity = 0.6,
                popup = f"{ip}",
            ).add_to(m)

        '''
        if last_ip != None:
            p_a = [data[ip]["lat"], data[ip]["long"]]
            p_b = [data[last_ip]["lat"], data[last_ip]["long"]]
            folium.PolyLine(
                locations=[p_a, p_b],
                color="red",
                weight=2,
                opacity=0.4
            ).add_to(m)
        last_ip = ip'''


    m.save("map.html")
    print("✅ Carte enregistrée dans map.html")

create_map_from_routers_pos(ROUTERS_POSITION_FILE_NAME)
'''
with open(REPORTS_FILE_NAME, 'r') as f:
    data = json.load(f)

# For each report
routers = data["2025-10-24T16:26:06+02:00"]["hubs"]

points = {}
# TODO: ajouter les pertes dans le popup
# Recrée un dictionnaire dont les clés sont les adresses IP
for report in data:
    for router in data[report]["hubs"]:
        ip_address = router["host"]

        if ip_address == "???":
            continue

        if ip_address in points:
            points[ip_address]["nb_times_encountered"] += 1
        else:
            p = {
                "order": router["count"],
                "lat": 0,
                "long": 0,
                "nb_times_encountered": 1,
            }

            points[ip_address] = p

first_key = next(iter(points))

# Création de la carte
m = folium.Map(location=[points[first_key]["lat"], points[first_key]["long"]], zoom_start=5)
last_ip = None

for ip in points:
    # Get more in-depth info on those IP addresses
    url = f"https://ipinfo.io/{ip}"
    #response = requests.get(url, PARAMS)
    response = requests.get(url)

    if response.status_code == 200:
        if "loc" in response.json():
        # On utilise le champ 'ip' de la réponse pour être sûr qu'on parle de la bonne adresse ip
            ip = response.json()["ip"]

            if ip in points:
                lat, long = response.json()["loc"].split(",")
                points[ip]["lat"] = float(lat)
                points[ip]["long"] = float(long)
            else:
                print(f"Error: response for non existing ip: {ip}")

            folium.CircleMarker(
                location = [points[ip]["lat"], points[ip]["long"]],
                radius=points[ip]["nb_times_encountered"],
                color = "red",
                fill = True,
                fill_color = "red",
                fill_opacity = 0.6,
                popup = f"{ip}",
            ).add_to(m)

        # TODO: Problème: ils sont pas dans le bon ordre, ils sont dans l'ordre des réponses reçues par la requête à ipinfo.io
        if last_ip != None:
            p_a = [points[ip]["lat"], points[ip]["long"]]
            p_b = [points[last_ip]["lat"], points[last_ip]["long"]]
            folium.PolyLine(
                locations=[p_a, p_b],
                color="red",
                weight=2,
                opacity=0.4
            ).add_to(m)
        last_ip = ip

    else:
        print(f"Error at IP {ip}: {response.status_code}")

# Sauvegarde la position des routeurs dans un JSON
with open("routers_pos.json", "w", encoding="utf-8") as f:
    json.dump(points, f, ensure_ascii=False, indent=4)
    

'''