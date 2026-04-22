import requests
import pandas as pd
import os
from datetime import datetime

# URL Spotify Global Daily
URL = "https://kworb.net/spotify/country/global_daily.html"
LOG_FILE = "novita_classifiche.txt"

def recupera_spotify_top():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers)
        # Usiamo lxml come motore di lettura se disponibile, altrimenti quello base
        tabelle = pd.read_html(response.content, encoding='utf-8')
        
        # La classifica Spotify è solitamente la prima tabella (indice 0)
        df = tabelle[0]
        
        # Pulizia: su Spotify la colonna Artist and Title è quasi sempre la seconda (indice 1)
        # ma proviamo a cercarla per nome per sicurezza
        colonna_target = None
        for col in df.columns:
            if 'Artist and Title' in str(col):
                colonna_target = col
                break
        
        if colonna_target is not None:
            brani = df.head(100)[colonna_target].tolist()
        else:
            # Fallback sulla seconda colonna
            brani = df.head(100).iloc[:, 1].tolist()
            
        return set(brani)
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
    # Filtriamo nan e stringhe troppo corte (possibili errori di lettura)
    nuove_entrate = [b for b in attuali if pd.notna(b) and len(str(b)) > 5 and b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] SPOTIFY NEW: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
        
