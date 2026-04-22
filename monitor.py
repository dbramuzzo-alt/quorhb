import requests
import pandas as pd
import os
import io
from datetime import datetime

# Configurazione
URL = "https://kworb.net/ww/" 
LOG_FILE = "novita_classifiche.txt"

def recupera_top_100():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers)
        # Usiamo io.StringIO per assicurarci che Pandas legga il testo e non cerchi un file
        tabelle = pd.read_html(io.StringIO(response.text))
        
        # La classifica Worldwide iTunes è la prima tabella
        df = tabelle[0]
        
        # Cerchiamo la colonna "Artist and Title"
        colonna_nomi = [c for c in df.columns if 'Artist' in str(c)]
        
        if colonna_nomi:
            brani = df.head(100)[colonna_nomi[0]].tolist()
        else:
            # Fallback sulla colonna indice 1 (la seconda)
            brani = df.head(100).iloc[:, 1].tolist()
            
        return set(brani)
    except Exception as e:
        print(f"Errore iTunes: {e}")
        return None

# Carica lo storico dal file
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

attuali = recupera_top_100()

if attuali:
    # Filtriamo via dati sporchi o troppo brevi
    nuove_entrate = [b for b in attuali if pd.notna(b) and len(str(b)) > 5 and b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] NUOVA: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
        
