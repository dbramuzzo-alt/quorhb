import requests
import pandas as pd
import os
from datetime import datetime

# Configurazione
URL = "https://kworb.net/itunes/" 
LOG_FILE = "novita_classifiche.txt"

def recupera_top_100():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(URL, headers=headers)
        tabelle = pd.read_html(response.text)
        df = max(tabelle, key=len) 
        
        # CERCHIAMO LA COLONNA CORRETTA
        # Kworb a volte cambia posizione, quindi cerchiamo la colonna che contiene testo lungo
        # Invece di usare un numero fisso, cerchiamo la colonna "Artist and Title"
        colonna_nomi = [c for c in df.columns if 'Artist' in str(c)]
        
        if colonna_nomi:
            brani = df.head(100)[colonna_nomi[0]].tolist()
        else:
            # Se non trova la colonna col nome, proviamo la seconda colonna (indice 1)
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
    # Filtriamo via eventuali simboli strani rimasti
    nuove_entrate = [b for b in attuali if len(str(b)) > 5 and b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] NUOVA: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
        
