from googleapiclient.discovery import build
import pandas as pd
import os
from dotenv import load_dotenv


# --- 1. UWIERZYTELNIANIE I KONFIGURACJA ---

load_dotenv()
API_KEY = os.getenv('YOUTUBE_API_KEY')

# Inicjalizujemy klienta API YouTube (używamy wersji 3)
youtube = build('youtube', 'v3', developerKey=API_KEY)

def analyze_youtube_topic(search_query):
    print(f"Searching YouTube for query: '{search_query}'...")

    # --- 2. First endpoint: search.list ---
    # Wyszukujemy 50 najbardziej trafnych filmów dla naszego zapytania.
    # Używamy parametru part='snippet', aby pobrać podstawowe informacje (jak tytuł).
    search_request = youtube.search().list(
        q=search_query,
        part='snippet',
        type='video',
        maxResults=50
    )
    search_response = search_request.execute()

    # Tworzymy puste listy, do których będziemy wrzucać identyfikatory (ID) i tytuły filmów
    video_ids = []
    video_titles = []
    
    # Przechodzimy przez każdy film z wyników wyszukiwania i wyciągamy z niego dane
    for item in search_response['items']:
        video_ids.append(item['id']['videoId'])
        video_titles.append(item['snippet']['title'])

    # --- 3. Second endpoint: videos.list ---
    # Pierwszy endpoint nie zwraca nam dokładnych statystyk (np. liczby wyświetleń).
    # Musimy połączyć zebrane ID filmów w jeden ciąg znaków (oddzielony przecinkami),
    # a następnie wysłać je do drugiego endpointu, który obsługuje statystyki.
    video_ids_string = ','.join(video_ids) 
    
    # Używamy parametru part='statistics', aby odpytać o wyświetlenia, lajki i komentarze
    video_request = youtube.videos().list(
        part='statistics',
        id=video_ids_string
    )
    video_response = video_request.execute()

    # Tworzymy nową listę, w której połączymy tytuły ze statystykami
    video_data = []
    for i, item in enumerate(video_response['items']):
        stats = item['statistics']
        # .get('nazwa', 0) zabezpiecza nasz kod - jeśli film ma wyłączone komentarze 
        # i API ich nie zwróci, kod wstawi tam domyślnie '0' zamiast wywalać błąd.
        video_data.append({
            'Title': video_titles[i],
            'Views': int(stats.get('viewCount', 0)),
            'Likes': int(stats.get('likeCount', 0)),
            'Comments': int(stats.get('commentCount', 0))
        })

    # --- 4. DODATEK ANALIZA DANYCH Z PANDAS ---
    # Konwertujemy zebrane "surowe" dane na czytelną tabelę (DataFrame) z biblioteki Pandas
    df = pd.DataFrame(video_data)
    
    # Obliczamy własną metrykę: Wskaźnik zaangażowania (Engagement Rate).
    # Wzór to: (Lajki + Komentarze) podzielone przez Wyświetlenia, pomnożone przez 100%.
    df['Engagement Rate (%)'] = ((df['Likes'] + df['Comments']) / df['Views'] * 100).round(2)
    
    # Sortujemy tabelę malejąco według liczby wyświetleń (najpopularniejsze na samej górze)
    df = df.sort_values(by='Views', ascending=False)
    
    # Eksportujemy naszą gotową, posortowaną tabelę do pliku CSV (idealne do analizy biznesowej np. w Excelu)
    csv_filename = 'youtube_analysis.csv'
    df.to_csv(csv_filename, index=False)
    
    print(f"\nSuccess! Data has been analyzed and saved to file {csv_filename}")
    return df

# Ten blok uruchamia się tylko wtedy, gdy odpalamy ten konkretny skrypt bezpośrednio w terminalu
if __name__ == "__main__":
    # Tutaj wywołujemy naszą funkcję. Możesz zmienić "Python programming tutorial" na cokolwiek chcesz!
    df_results = analyze_youtube_topic("Python programming tutorial")
    
    # Wypisujemy 5 najpopularniejszych filmów w czytelnej formie prosto do terminala, żeby móc je zaprezentować na wideo
    print("\nTop 5 video with the most views:")
    print(df_results.head(5).to_string())