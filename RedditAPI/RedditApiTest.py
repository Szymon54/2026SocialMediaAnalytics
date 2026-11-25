import requests

url = "https://www.reddit.com/r/Finland/hot.json"

# Używamy oficjalnego formatu nagłówka wymaganego przez Reddita dla skryptów
headers = {
    "User-Agent": "python:projekt_szkolny_hamk:v1.0 (by /u/szymon)"
}

params = {
    "limit": 3
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print("Sukces! Pobrano dane z Reddit API.\n")
    
    posts = data['data']['children']
    for i, post in enumerate(posts, 1):
        title = post['data']['title']
        print(f"{i}. {title}")
else:
    print(f"Błąd: {response.status_code}")
    print("Szczegóły:", response.text)