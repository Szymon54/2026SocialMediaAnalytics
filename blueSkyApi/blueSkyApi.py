import requests

# Zmieniamy cel na otwarte API Bluesky
adres_url = "https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed"

# Parametry zapytania: od kogo pobieramy (actor) i ile postów (limit)
parametry = {
    "actor": "jay.bsky.team", 
    "limit": 10
}

# Wysyłamy zapytanie (tutaj nie musimy udawać przeglądarki, wpuszczają nas oficjalnie)
odpowiedz = requests.get(adres_url, params=parametry)

print("Status zapytania:", odpowiedz.status_code)

if odpowiedz.status_code == 200:
    dane_z_bluesky = odpowiedz.json()
    print("Sukces! Bluesky nas wpuściło.\n")
    
    # Wyciągamy posty
    posty = dane_z_bluesky.get('feed', [])
    for numer, element in enumerate(posty, 1):
        # Docieramy do tekstu posta
        tresc = element['post']['record']['text']
        autor = element['post']['author']['handle']
        # Drukujemy pierwsze 80 znaków tekstu, żeby ładnie wyglądało w terminalu
        print(f"{numer}. [{autor}]: {tresc[:80]}...")
else:
    print("Błąd serwera:", odpowiedz.text)