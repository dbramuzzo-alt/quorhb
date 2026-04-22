import requests
import re
import os
from datetime import datetime

# URL della classifica ufficiale TikTok Billboard
URL = "https://www.billboard.com/charts/tiktok-billboard-top-50/"
LOG_FILE = "novita_classifiche.txt"

def recupera_tiktok_billboard():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(URL, headers=headers, timeout=30)
        response.encoding = 'utf-8'
        html = response.text

        # Usiamo le espressioni regolari per trovare i titoli dei brani
        # Billboard usa tag h3 con classi specifiche per i titoli
        # Cerchiamo i pattern più comuni nel loro codice
        c_titoli = re.findall(r'<h3[^>]*id="title-of-a-story"[^>]*>\s*([^<]+)\s*</h3>', html)
        # Cerchiamo gli artisti (solitamente sono span sotto i titoli)
        c_artisti = re.findall(r'<span[^>]*class="[^"]*c-label[^"]*"[^>]*>\s*([^<]+)\s*</span>', html)

        brani = []
        # Pulizia dei risultati
        for t, a in zip([t.strip() for t in c_titoli], [a.strip() for a in c_artisti]):
            if t and a and len(t) > 1 and "Chart" not in t:
                entry = f"{a} - {t}"
                brani.append(entry)
        
        # Se non troviamo nulla con il primo metodo, proviamo un fallback più generico
        if not brani:
            # Cerca qualsiasi testo dentro h3 che sembri un titolo
            backup = re.findall(r'c-title__link">([^<]+)</a>', html)
            brani = [b.strip() for b in backup if len(b) > 2]

        return set(brani)
    except Exception as e:
        print(f"Errore tecnico: {e}")
        return None

# Carica lo storico
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        storico = f.read()
else:
    storico = ""

attuali = recupera_tiktok_billboard()

if attuali:
    nuove_entrate = [b for b in attuali if b not in storico and "Songwriter" not in b]
    
    if nuove_entrate:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for canzone in nuove_entrate:
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M')
                f.write(f"[{timestamp}] TIKTOK TREND: {canzone}\n")
        print("FOUND")
    else:
        print("NO_CHANGES")
else:
    print("EMPTY_RESULTS")
    
