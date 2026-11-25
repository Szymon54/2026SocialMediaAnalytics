import googleapiclient.discovery

from env import API_KEY
CHANNEL_HANDLE = "MrBeast"


youtube = googleapiclient.discovery.build(
    "youtube", 
    "v3", 
    developerKey=API_KEY)

#Endpoint: Get the channel information
response = youtube.channels().list(
    part="snippet,statistics,contentDetails",
    forHandle=CHANNEL_HANDLE
).execute()

channel = response["items"][0]

print("Channel Name: ",
      channel["snippet"]["title"])

print("Subscribers: ",
      channel["statistics"]["subscriberCount"])

print("Total Views: ",
      channel["statistics"]["viewCount"])

print("Videos: ",
      channel["statistics"]["videoCount"])