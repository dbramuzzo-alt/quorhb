import requests
import pandas as pd
import os
from datetime import datetime

# URL per Spotify Global Daily
URL = "https://kworb.net/spotify/country/global_daily.html"
LOG_FILE = "novita_classifiche.txt"

def recupera_spotify_top():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers)
        # Kworb mette la tabella Spotify come prima tabella
        tabelle = pd.read_html(response.content, encoding='utf-8')
        df = tabelle[0]
        
        # Cerchiamo la colonna "Artist and Title"
        if 'Artist and Title' in df.columns:
            brani = df.head(100)['Artist and Title'].tolist()
        else:
            brani = df.head(100).iloc[:, 1].tolist()
            
        return set(brani)
    except Exception as e:
        print(f"Errore Spotify: {e}")
        return None

# Carica lo storico esistente
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

attuali = recupera_spotify_top()

if attuali:
    # Cerchiamo canzoni nuove per Spotify
    nuove_entrate = [b for b in attuali if str(b) != 'nan' and b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] SPOTIFY NEW: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
