import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 1. Määritellään tiedostot ja asetukset
csv_file = 'stats.csv'
img_file = 'stats.png'
api_url = "https://wiki.isosten.net/api.php?action=query&meta=siteinfo&siprop=statistics&format=json"

# 2. Haetaan tuoreimmat tiedot wikistä
try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    data = response.json()
    stats = data['query']['statistics']
except Exception as e:
    print(f"Virhe haettaessa tietoja API:sta: {e}")
    exit(1)

today = datetime.now().strftime("%Y-%m-%d")
new_entry = {
    'date': today,
    'pages': stats['pages'],
    'edits': stats['edits'],
    'users': stats['users']
}

# 3. Luetaan vanha historia tai luodaan uusi, jos tiedosto puuttuu tai on tyhjä
if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    try:
        df = pd.read_csv(csv_file)
    except Exception:
        # Jos luku epäonnistuu (esim. korruptoitunut tiedosto), aloitetaan alusta
        df = pd.DataFrame(columns=['date', 'pages', 'edits', 'users'])
else:
    df = pd.DataFrame(columns=['date', 'pages', 'edits', 'users'])

# 4. Lisätään uusi rivi vain, jos tälle päivälle ei vielä ole merkintää
if today not in df['date'].values:
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(csv_file, index=False)
    print(f"Päivitetty tilastot päivälle {today}")
else:
    print("Tämän päivän tilastot ovat jo tallennettu.")

# 5. Luodaan graafi
if len(df) > 0:
    plt.figure(figsize=(10, 6))
    
    # Piirretään viivat (käytetään kakkosakselia, jos luvuissa on suuri ero)
    plt.plot(df['date'], df['pages'], marker='o', linestyle='-', color='blue', label='Sivuja')
    plt.plot(df['date'], df['users'], marker='s', linestyle='--', color='green', label='Käyttäjiä')

    plt.title('Wiki.isosten.net kasvu', fontsize=14)
    plt.xlabel('Päivämäärä')
    plt.ylabel('Määrä')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()

    # Tallennetaan kuva
    plt.savefig(img_file)
    print("Graafi päivitetty.")
