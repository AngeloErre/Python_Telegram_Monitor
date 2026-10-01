#!/bin/bash
# IT: Avvia il monitor dalla cartella del progetto.
# EN: Start the monitor from the project directory.
cd "$(dirname "$0")" || exit 1
python3 telegram_monitor.py
printf "\nMonitor stopped / Monitor terminato. Press a key to close..."
read -n 1 -s
