import requests
import pandas as pd
import os
from datetime import datetime

# URL specifico per le canzoni (Worldwide iTunes Song Chart)
URL = "https://kworb.net/ww/" 
LOG_FILE = "novita_classifiche.txt"

def recupera_top_100():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # Usiamo 'content' invece di 'text' per gestire correttamente gli accenti (Rosalía, ecc.)
        response = requests.get(URL, headers=headers)
        tabelle = pd.read_html(response.content, encoding='utf-8')
        
        # In questa pagina la classifica è la tabella principale
        df = tabelle[0]
        
        # La colonna con "Artista - Canzone" è quella chiamata 'Artist and Title'
        # Se non la trova per nome, usiamo la posizione (di solito la seconda colonna)
        if 'Artist and Title' in df.columns:
            brani = df.head(100)['Artist and Title'].tolist()
        else:
            brani = df.head(100).iloc[:, 1].tolist()
            
        return set(brani)
    except Exception as e:
        print(f"Errore: {e}")
        return None

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

attuali = recupera_top_100()

if attuali:
    # Cerchiamo le canzoni che non sono presenti nel file log
    nuove_entrate = [b for b in attuali if str(b) != 'nan' and b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] NUOVA: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
        
