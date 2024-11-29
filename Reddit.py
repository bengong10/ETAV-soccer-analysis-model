import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd

# Reddit API credentials
reddit = praw.Reddit(
    client_id="3Vd1VvjKFlNoft8q74PU1w",
    client_secret='_96HfhnxASTt-uNBZk090CA-REJH6g',  
    user_agent="SentimentAnalysisApp"
)


# Players and their transfer dates
player_data = [
    {"Player": "Rasmus Hojlund", "Transfer Date": "2023-08-05"},
    {"Player": "Andre Onana", "Transfer Date": "2023-07-20"},
    {"Player": "Mason Mount", "Transfer Date": "2023-07-05"},
    {"Player": "Antony", "Transfer Date": "2022-08-30"},
    {"Player": "Casemiro", "Transfer Date": "2022-08-22"},
    {"Player": "Lisandro Martínez", "Transfer Date": "2022-07-27"},
    {"Player": "Christian Eriksen", "Transfer Date": "2022-07-15"},
    {"Player": "Tyrell Malacia", "Transfer Date": "2022-07-05"},
    {"Player": "Cristiano Ronaldo", "Transfer Date": "2021-08-31"},
    {"Player": "Raphael Varane", "Transfer Date": "2021-08-14"},
    {"Player": "Jadon Sancho", "Transfer Date": "2021-07-23"}
]

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Results list
results = []

# Fetch Reddit posts for each player
for player in player_data:
    query = f"{player['Player']} transfer"
    print(f"Processing: {player['Player']}")

    try:
        # Search for posts related to the player
        posts = reddit.subreddit("soccer").search(query, limit=100)

        # Perform Sentiment Analysis
        sentiments = []
        for post in posts:
            sentiment_score = analyzer.polarity_scores(post.title)["compound"]
            sentiments.append(sentiment_score)

        # Calculate average sentiment and media coverage intensity
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        media_coverage_intensity = len(sentiments) * (1 + avg_sentiment)

        # Append results
        results.append({
            "Player": player["Player"],
            "Transfer Date": player["Transfer Date"],
            "Average Sentiment": avg_sentiment,
            "Media Coverage Intensity": media_coverage_intensity,
            "Posts Analyzed": len(sentiments)
        })

    except Exception as e:
        print(f"Error processing {player['Player']}: {e}")
        results.append({
            "Player": player["Player"],
            "Transfer Date": player["Transfer Date"],
            "Average Sentiment": "Error",
            "Media Coverage Intensity": "Error",
            "Posts Analyzed": "Error"
        })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Display results
print(results_df)

# Save results to CSV
results_df.to_csv("reddit_sentiment_results.csv", index=False)
