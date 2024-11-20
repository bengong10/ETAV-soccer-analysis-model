import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# NewsData.io API setup
api_key = "pub_59566c309eb7bf865216c9c4a588dc3b6b6ab"
base_url = "https://newsdata.io/api/1/news"

# List of players
players = [
    "Rasmus Hojlund", "Andre Onana", "Mason Mount", "Antony", "Casemiro",
    "Lisandro Martínez", "Christian Eriksen", "Tyrell Malacia",
    "Cristiano Ronaldo", "Raphael Varane", "Jadon Sancho"
]

# Initialize results list
results = []

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Loop through each player
for player in players:
    print(f"Processing: {player}")
    params = {
        "apikey": api_key,
        "q": f"{player} transfer",
        "language": "en"
    }
    try:
        # Fetch data from NewsData.io API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        # Extract relevant articles
        articles = data.get("results", [])
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")

            # Calculate sentiment for title and description
            title_sentiment = analyzer.polarity_scores(title)['compound'] if title else 0
            description_sentiment = analyzer.polarity_scores(description)['compound'] if description else 0

            # Store results
            results.append({
                "Player": player,
                "Title": title,
                "Description": description,
                "Source": article.get("source_id"),
                "Link": article.get("link"),
                "Published Date": article.get("pubDate"),
                "Title Sentiment": title_sentiment,
                "Description Sentiment": description_sentiment,
            })

    except Exception as e:
        print(f"Error processing {player}: {e}")

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Save results to a CSV file
results_df.to_csv('player_transfer_news_with_sentiment.csv', index=False)

# Display a sample of the results
print("Sample Results with Sentiment:")
print(results_df.head())
