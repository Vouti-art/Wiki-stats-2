import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

# 1. Hae tiedot wikistä
API_URL = "https://wiki.isosten.net/api.php?action=query&meta=siteinfo&siprop=statistics&format=json"
data = requests.get(API_URL).json()
stats = data['query']['statistics']
today = datetime.now().strftime("%Y-%m-%d")

# 2. Päivitä CSV-tiedosto
csv_file = 'stats.csv'
new_data = pd.DataFrame([{
    'date': today,
    'pages': stats['pages'],
    'edits': stats['edits'],
    'users': stats['users']
}])

if os.path.exists(csv_file) and os.path.getsize(csv_file) > 0:
    try:
        df = pd.read_csv(csv_file)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=['date', 'pages', 'edits', 'users'])
else:
    # Jos tiedostoa ei ole tai se on tyhjä, luodaan uusi DataFrame sarakkeilla
    df = pd.DataFrame(columns=['date', 'pages', 'edits', 'users'])
    # Lisätään uusi rivi vain jos tälle päivälle ei vielä ole tietoa
    if today not in df['date'].values:
        df = pd.concat([df, new_data], ignore_index=True)
else:
    df = new_data

df.to_csv(csv_file, index=False)

# 3. Luodaan graafi
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['pages'], marker='o', label='Sivuja')
plt.plot(df['date'], df['users'], marker='s', label='Käyttäjiä')

plt.title('Wiki.isosten.net kasvu')
plt.xlabel('Päivämäärä')
plt.ylabel('Määrä')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Tallennetaan kuvatiedostona
plt.savefig('stats.png')
