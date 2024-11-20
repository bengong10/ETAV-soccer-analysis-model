import requests
import pandas as pd

# Bing News Search API setup
subscription_key = "4423c5aa-6f01-45fc-8a53-fb534c28f747"
endpoint = "https://api.bing.microsoft.com/v7.0/news/search"

# List of players
players = [
    "Rasmus Hojlund", "Andre Onana", "Mason Mount", "Antony", "Casemiro",
    "Lisandro Martínez", "Christian Eriksen", "Tyrell Malacia",
    "Cristiano Ronaldo", "Raphael Varane", "Jadon Sancho"
]


results = []

for player in players:
    params = {
        "q": f"{player} transfer",
        "count": 20,
        "mkt": "en-US",
    }
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.get(endpoint, headers=headers, params=params)
    data = response.json()
    articles = data.get("value", [])
    results.append({"Player": player, "Articles": len(articles)})

# Convert to DataFrame
df = pd.DataFrame(results)
print(df)
