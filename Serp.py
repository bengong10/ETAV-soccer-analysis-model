from serpapi import GoogleSearch
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# SerpAPI setup
api_key = "EFB65F4E0F254F0B9EC6C91F5F9C0770"  
search_engine = "google_news"  # Search engine type

# List of players
players = [
    "Rasmus Højlund", "André Onana", "Mason Mount", "Antony", "Casemiro",
    "Lisandro Martínez", "Christian Eriksen", "Tyrell Malacia",
    "Cristiano Ronaldo", "Raphaël Varane", "Jadon Sancho"
]

# Initialize results list
results = []

# Initialize VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Loop through players to get news
for player in players:
    print(f"Processing: {player}")

    try:
        # Define query
        query = f"{player} transfer"

        # Perform SerpAPI search
        search = GoogleSearch({
            "q": query,
            "tbm": "nws",  # News search
            "api_key": api_key,
            "num": 20  # Number of results to fetch
        })
        response = search.get_dict()

        # Extract articles
        articles = response.get("news_results", [])

        if articles:
            # Convert articles to a DataFrame
            df = pd.DataFrame(articles)

            # Analyze sentiment of article titles
            df["sentiment"] = df["title"].apply(lambda x: analyzer.polarity_scores(x)['compound'] if pd.notnull(x) else 0)

            # Calculate Media Coverage Intensity
            df["intensity"] = 1 + df["sentiment"]
            media_coverage_intensity = df["intensity"].sum()
        else:
            media_coverage_intensity = 0

        # Append result
        results.append({"Player": player, "Media Coverage Intensity": media_coverage_intensity})

    except Exception as e:
        print(f"Error processing {player}: {e}")
        results.append({"Player": player, "Media Coverage Intensity": "Error"})

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Display results
print(results_df)

# Save results to a CSV file
results_df.to_csv("serpapi_media_coverage.csv", index=False)
