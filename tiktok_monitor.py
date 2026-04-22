import requests
import pandas as pd
import os
import io
from datetime import datetime

# URL della classifica ufficiale TikTok Billboard
URL = "https://www.billboard.com/charts/tiktok-billboard-top-50/"
LOG_FILE = "novita_classifiche.txt"

def recupera_tiktok_billboard():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        
        # Billboard ha una struttura complessa, quindi cerchiamo i dati in modo mirato
        # Leggiamo le tabelle (Billboard spesso ne usa una per la chart)
        tabelle = pd.read_html(io.StringIO(response.text))
        
        # Cerchiamo la tabella che contiene i dati (solitamente la prima o l'unica con molti dati)
        df = tabelle[0]
        
        # Pulizia: Billboard usa spesso colonne con nomi come 'Song' o 'Artist'
        # Cerchiamo di estrarre le prime 30-40 righe che sono il cuore del trend
        brani = []
        for index, row in df.head(50).iterrows():
            # Uniamo le celle della riga per trovare il nome del brano e artista
            info = " - ".join([str(val) for val in row if pd.notna(val) and "RANK" not in str(val).upper()])
            brani.append(info)
            
        return set([b.encode('utf-8', 'ignore').decode('utf-8') for b in brani])
    except Exception:
        # Se pandas fallisce (perché Billboard cambia layout), usiamo un metodo di emergenza
        print("Errore lettura tabella Billboard")
        return None

# Carica lo storico
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

attuali = recupera_tiktok_billboard()

if attuali:
    nuove_entrate = [b for b in attuali if len(str(b)) > 10 and b not in storico]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] TIKTOK TREND: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
        
