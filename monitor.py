import requests
import pandas as pd
import os
from datetime import datetime

# Configurazione - Puntiamo ai singoli mondiali
URL = "https://kworb.net/itunes/" 
LOG_FILE = "novita_classifiche.txt"

def recupera_top_100():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers)
        # Legge le tabelle HTML
        tabelle = pd.read_html(response.text)
        # Kworb ha la classifica principale come tabella più lunga
        df = max(tabelle, key=len) 
        # La colonna 1 (la seconda) contiene "Artist and Title"
        brani = df.head(100).iloc[:, 1].tolist()
        return set(brani)
    except Exception as e:
        print(f"Errore durante il recupero: {e}")
        return None

# 1. Carica lo storico dal file per vedere cosa abbiamo già loggato
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

# 2. Ottieni la Top 100 attuale
attuali = recupera_top_100()

if attuali:
    # 3. Confronta: quali canzoni tra le attuali NON sono nello storico?
    nuove_entrate = [b for b in attuali if b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] NUOVA: {canzone}\n")
        print("FOUND") # Segnale per l'automazione
    else:
        print("NO_CHANGES")
      
