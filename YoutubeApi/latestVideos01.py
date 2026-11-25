import googleapiclient.discovery

from env import API_KEY
CHANNEL_HANDLE = "Fireship"


youtube = googleapiclient.discovery.build(
    "youtube", 
    "v3", 
    developerKey=API_KEY)

#Endpoint: Get the channel information
channel_request = youtube.channels().list(
    part="contentDetails",
    forHandle=CHANNEL_HANDLE
)

channel_response = channel_request.execute()

channel = channel_response["items"][0]

# Endpoint: Get the latest 20 videos
uploads_playlist_id = (
    channel ["contentDetails"]
            ["relatedPlaylists"]
            ["uploads"]
)

print("Upload Playlist ID:")
print(uploads_playlist_id)



video_request = youtube.playlistItems().list(
    part="snippet",
    playlistId=uploads_playlist_id, 
    maxResults=20
)

videos_response = video_request.execute()

print("\nLatest 20 Videos:")
print("-", 60)

for index, item in enumerate(videos_response["items"], start=1):
    title = item["snippet"]["title"]
    published = item["snippet"]["publishedAt"]
    print(f"{index}. {title} ")
    print(f"   Published: {published}")
    print()