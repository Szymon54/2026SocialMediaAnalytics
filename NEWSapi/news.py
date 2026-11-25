import requests

# Import the API key from the env module
from env import api_key

# Define the URL for the News API request
# f-string tells Python that this is a formatted string &
# it allows insert variables or expressions directly into a string using curly brackets {}.
url = f"https://newsapi.org/v2/everything?q=Jensen Huang&apiKey={api_key}"

# Make a GET request to the News API
response = requests.get(url)

# Parse the JSON response from the API
data = response.json()

# Extract the titles of all articles from the response
titles = [article['title'] for article in data['articles']]

# Limit the list to the first 50 titles
limited_titles = titles[:50]

# Print the list of limited article titles as a numbered list
for i, title in enumerate(limited_titles, start=1):
    print(f"{i}. {title}")

#run .\news.py in terminal to see the output