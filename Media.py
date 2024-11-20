import requests
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# List of player names
players = [
    "Rasmus Hojlund", "Andre Onana", "Mason Mount", "Antony", "Casemiro",
    "Lisandro Martínez", "Christian Eriksen", "Tyrell Malacia",
    "Cristiano Ronaldo", "Raphael Varane", "Jadon Sancho"
]

# GDELT API base URL
base_url = "https://api.gdeltproject.org/api/v2/doc/doc"

# Initialize results list
results = []

# Sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Loop through each player
for player in players:
    print(f"Processing: {player}")
    params = {
        "query": f'"{player} transfer"',
        "mode": "ArtList",  # List of matching articles
        "maxrecords": 100,  # Maximum number of results
        "format": "json"    # Response format
    }
    try:
        # Fetch data from GDELT API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        data = response.json()

        # Extract articles
        articles = data.get("articles", [])
        if articles:
            df = pd.DataFrame(articles)
            # Calculate sentiment
            df['sentiment'] = df['title'].apply(lambda x: analyzer.polarity_scores(x)['compound'] if pd.notnull(x) else 0)
            # Calculate media coverage intensity
            df['intensity'] = 1 + df['sentiment']  # Simple weighting
            media_coverage_intensity = df['intensity'].sum()
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
results_df.to_csv('media_coverage_intensity.csv', index=False)
