#!/usr/bin/env bash
set -euo pipefail

while true; do
    sudo /opt/homebrew/Cellar/mtr/0.96/sbin/mtr -n -r -c 10 baidu.com --json | jq --arg ts "$(date -Iseconds)" '{($ts): .report}' > r.json
    jq '. as $r | . = input | . + $r' r.json reports.json > tmp.json && mv tmp.json reports.json
    rm r.json
    echo "** Ping Report created at $(date -Iseconds) **"
    sleep 3600
done