#!/bin/bash

IP="220.181.7.203"
CSV_FILE="ping_results.csv"

# Vérifie si le CSV existe, sinon crée l'en-tête
if [ ! -f "$CSV_FILE" ]; then
    echo "Date,Avg RTT (ms)" > "$CSV_FILE"
fi

while true; do
    current_time=$(date "+%Y-%m-%d %H:%M")
    # Exécuter le ping et extraire le temps moyen
    ping_result=$(ping -c 10 $IP | grep "round-trip")
    avg_rtt=$(echo "$ping_result" | awk -F '/' '{print $5}')

    # Ajouter dans le CSV
    echo "$current_time,$avg_rtt" >> "$CSV_FILE"

    echo "Sauvegardé. "$current_time,$avg_rtt ms""

    sleep 1800
done
