import requests
import pandas as pd
import os
import io
from datetime import datetime

# Configurazione Spotify Global Daily
URL = "https://kworb.net/spotify/country/global_daily.html"
LOG_FILE = "novita_classifiche.txt"

def recupera_spotify_top():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers)
        # StringIO risolve l'errore "No such file or directory" interpretando l'HTML come testo
        tabelle = pd.read_html(io.StringIO(response.text))
        
        # La classifica Spotify su Kworb è solitamente la prima tabella
        df = tabelle[0]
        
        # Cerchiamo la colonna corretta (Artist and Title)
        colonna_target = None
        for col in df.columns:
            if 'Artist and Title' in str(col):
                colonna_target = col
                break
        
        if colonna_target:
            brani = df.head(100)[colonna_target].tolist()
        else:
            # Fallback sulla colonna indice 1 (la seconda)
            brani = df.head(100).iloc[:, 1].tolist()
            
        return set(brani)
    except Exception as e:
        print(f"Errore Spotify: {e}")
        return None

# Carica lo storico dal file per evitare duplicati
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

attuali = recupera_spotify_top()

if attuali:
    # Filtriamo nan e brani già presenti nel diario (sia da iTunes che Spotify)
    nuove_entrate = [b for b in attuali if pd.notna(b) and len(str(b)) > 5 and b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] SPOTIFY NEW: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
        
