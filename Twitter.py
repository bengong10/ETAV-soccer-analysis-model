import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import time

# Twitter API v2 credentials
bearer_token = "AAAAAAAAAAAAAAAAAAAAABkuxAEAAAAANLI0F017f1L2YATKWYiseGONrHM%3DQ69HQ1X5lPWPEPSMpLCQHAXx10Tk219lGDkYtynOGUR50mxM1C"

# Initialize Tweepy client
client = tweepy.Client(bearer_token=bearer_token)

# Players and their transfer dates
player_data = [
    {"Player": "Jadon Sancho", "Transfer Date": "2024-11-11"},
    {"Player": "Cristiano Ronaldo", "Transfer Date": "2024-11-11"},
    # Add more players here
]

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Results list
results = []


# Function to handle exponential backoff
def exponential_backoff(retries):
    delay = min(60, (2 ** retries))  # Cap delay at 60 seconds
    print(f"Rate limit hit. Retrying in {delay} seconds...")
    time.sleep(delay)


# Fetch tweets for each player (with retry logic)
for player in player_data:
    query = f"{player['Player']} transfer"
    start_time = f"{player['Transfer Date']}T00:00:00Z"  # ISO 8601 format
    retries = 0
    max_retries = 5  # Maximum number of retries
    success = False

    print(f"Processing: {player['Player']}")

    while not success and retries <= max_retries:
        try:
            # Fetch up to 10 tweets for each query
            response = client.search_recent_tweets(
                query=query,
                start_time=start_time,
                max_results=10,  # Limit results to 10
                tweet_fields=["text", "created_at"]
            )

            tweets = response.data if response.data else []

            # Perform Sentiment Analysis
            sentiments = []
            for tweet in tweets:
                sentiment_score = analyzer.polarity_scores(tweet.text)["compound"]
                sentiments.append(sentiment_score)

            # Calculate average sentiment and media coverage intensity
            avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
            media_coverage_intensity = len(tweets) * (1 + avg_sentiment)

            # Append results
            results.append({
                "Player": player["Player"],
                "Transfer Date": player["Transfer Date"],
                "Average Sentiment": avg_sentiment,
                "Media Coverage Intensity": media_coverage_intensity,
                "Tweets Analyzed": len(tweets),
                "Error Message": None
            })

            success = True  # Break out of retry loop on success

        except tweepy.errors.TooManyRequests as e:
            retries += 1
            if retries > max_retries:
                print(f"Max retries exceeded for {player['Player']}. Skipping...")
                results.append({
                    "Player": player["Player"],
                    "Transfer Date": player["Transfer Date"],
                    "Average Sentiment": "Error",
                    "Media Coverage Intensity": "Error",
                    "Tweets Analyzed": "Error",
                    "Error Message": str(e)
                })
                break
            exponential_backoff(retries)

        except Exception as e:
            print(f"Error processing {player['Player']}: {e}")
            results.append({
                "Player": player["Player"],
                "Transfer Date": player["Transfer Date"],
                "Average Sentiment": "Error",
                "Media Coverage Intensity": "Error",
                "Tweets Analyzed": "Error",
                "Error Message": str(e)
            })
            break

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# Display results
print(results_df)

# Save results to CSV
results_df.to_csv("twitter_with_backoff_results.csv", index=False)
