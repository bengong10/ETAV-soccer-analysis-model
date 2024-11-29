import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from datetime import datetime

# Reddit API credentials
reddit = praw.Reddit(
    client_id="3Vd1VvjKFlNoft8q74PU1w",
    client_secret='_96HfhnxASTt-uNBZk090CA-REJH6g',
    user_agent="SentimentAnalysisApp"
)

# Players and their transfer/season-end dates
player_data = [
    {"Player": "Rasmus Hojlund", "Transfer Date": "2023-08-05", "Season End Date": "2024-05-19"},
    {"Player": "Andre Onana", "Transfer Date": "2023-07-20", "Season End Date": "2024-05-19"},
    {"Player": "Mason Mount", "Transfer Date": "2023-07-05", "Season End Date": "2024-05-19"},
    {"Player": "Antony", "Transfer Date": "2022-08-30", "Season End Date": "2023-05-28"},
    {"Player": "Casemiro", "Transfer Date": "2022-08-22", "Season End Date": "2023-05-28"},
    {"Player": "Lisandro Martínez", "Transfer Date": "2022-07-27", "Season End Date": "2023-05-28"},
    {"Player": "Christian Eriksen", "Transfer Date": "2022-07-15", "Season End Date": "2023-05-28"},
    {"Player": "Tyrell Malacia", "Transfer Date": "2022-07-05", "Season End Date": "2023-05-28"},
    {"Player": "Cristiano Ronaldo", "Transfer Date": "2021-08-31", "Season End Date": "2022-05-22"},
    {"Player": "Raphael Varane", "Transfer Date": "2021-08-14", "Season End Date": "2022-05-22"},
    {"Player": "Jadon Sancho", "Transfer Date": "2021-07-23", "Season End Date": "2022-05-22"}
]

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Results list
results = []

# Fetch Reddit posts for each player
for player in player_data:
    query = f"{player['Player']} performance"
    transfer_date = datetime.strptime(player["Transfer Date"], "%Y-%m-%d")
    season_end_date = datetime.strptime(player["Season End Date"], "%Y-%m-%d")

    print(f"Processing: {player['Player']} (From {transfer_date} to {season_end_date})")

    try:
        # Search for posts related to the player
        posts = reddit.subreddit("soccer").search(query, limit=100)

        # Perform Sentiment Analysis
        sentiments = []
        for post in posts:
            post_date = datetime.utcfromtimestamp(post.created_utc)
            if transfer_date <= post_date <= season_end_date:
                sentiment_score = analyzer.polarity_scores(post.title)["compound"]
                sentiments.append(sentiment_score)

        # Calculate average sentiment and media coverage intensity
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        media_coverage_intensity = len(sentiments) * (1 + avg_sentiment)

        # Append results
        results.append({
            "Player": player["Player"],
            "Transfer Date": player["Transfer Date"],
            "Season End Date": player["Season End Date"],
            "Average Sentiment": avg_sentiment,
            "Media Coverage Intensity": media_coverage_intensity,
            "Posts Analyzed": len(sentiments)
        })

    except Exception as e:
        print(f"Error processing {player['Player']}: {e}")
        results.append({
            "Player": player["Player"],
            "Transfer Date": player["Transfer Date"],
            "Season End Date": player["Season End Date"],
            "Average Sentiment": "Error",
            "Media Coverage Intensity": "Error",
            "Posts Analyzed": "Error"
        })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Display results
print(results_df)

# Save results to CSV
results_df.to_csv("reddit_sentiment_results_season1.csv", index=False)
print("Results saved to 'reddit_sentiment_results_season1.csv'")
