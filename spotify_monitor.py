import requests
import pandas as pd
import os
import io
from datetime import datetime

URL = "https://kworb.net/spotify/country/global_daily.html"
LOG_FILE = "novita_classifiche.txt"

def recupera_spotify_top():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8' # <--- Fondamentale
        tabelle = pd.read_html(io.StringIO(response.text))
        df = tabelle[0]
        
        colonna_target = None
        for col in df.columns:
            if 'Artist and Title' in str(col):
                colonna_target = col
                break
        
        brani = df.head(100)[colonna_target].tolist() if colonna_target else df.head(100).iloc[:, 1].tolist()
        # Pulizia finale caratteri sporchi
        return set([str(b).encode('utf-8', 'ignore').decode('utf-8') for b in brani])
    except Exception as e:
        print(f"Errore Spotify: {e}")
        return None

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

attuali = recupera_spotify_top()

if attuali:
    nuove_entrate = [b for b in attuali if pd.notna(b) and len(str(b)) > 5 and b not in storico]
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] SPOTIFY NEW: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
        
