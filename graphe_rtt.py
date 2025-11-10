import csv
from datetime import datetime
import matplotlib.pyplot as plt

hours = []
rtt_values = []

with open("ping_results.csv", newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # convertir la date en datetime
        dt = datetime.strptime(row['Date'], "%Y-%m-%d %H:%M")
        hours.append(dt.hour)
        ms=row['Avg RTT (ms)']
        # Si une valeur a été mesurée
        if ms != '':
            rtt_values.append(float(row['Avg RTT (ms)']))

# Calc la moyenne du RTT par heure de la journée
rtt_per_hour = [0]*24
count_per_hour = [0]*24

for h, rtt in zip(hours, rtt_values):
    rtt_per_hour[h] += rtt
    count_per_hour[h] += 1

for i in range(24):
    if count_per_hour[i] > 0:
        rtt_per_hour[i] /= count_per_hour[i]

# Trace le graphe
plt.figure(figsize=(10,5))
plt.plot(range(24), rtt_per_hour, marker='o')
plt.xticks(range(24))
plt.xlabel("Heure")
plt.ylabel("RTT moyen (ms)")
plt.title("RTT moyen par heure vers baidu.com")
plt.grid(True)
plt.show()
