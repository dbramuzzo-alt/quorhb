import requests
import pandas as pd
import os
import io
from datetime import datetime

# URL di TokBoard (Classifica dei suoni trending)
URL = "https://tokboard.com/"
LOG_FILE = "novita_classifiche.txt"

def recupera_tiktok_trending():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers)
        response.encoding = 'utf-8'
        
        # TokBoard usa tabelle o strutture div. Pandas cercherà di estrarre il testo utile.
        # In questo caso leggiamo i titoli dei brani più popolari.
        tabelle = pd.read_html(io.StringIO(response.text))
        df = tabelle[0]
        
        # Pulizia: prendiamo i primi 50 trend (oltre diventano troppo di nicchia)
        # Solitamente la colonna con i nomi è la seconda o ha nomi specifici
        brani = df.head(50).iloc[:, 1].tolist()
            
        return set([str(b).encode('utf-8', 'ignore').decode('utf-8') for b in brani])
    except Exception as e:
        print(f"Errore TikTok Monitor: {e}")
        return None

# Carica lo storico
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

attuali = recupera_tiktok_trending()

if attuali:
    # Filtriamo ed evitiamo duplicati già presenti nel diario
    nuove_entrate = [b for b in attuali if pd.notna(b) and len(str(b)) > 5 and b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] TIKTOK TREND: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
