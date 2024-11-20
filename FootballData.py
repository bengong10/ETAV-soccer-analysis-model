import requests

# Player data with transfer dates
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

# Example API setup (e.g., Football Data API or another sports API)
api_key = "db63a07e1fc848059879023f77f4d767"
base_url = "https://api.football-data.org/v4"  # Example: Football-Data API
headers = {"X-Auth-Token": api_key}

# Initialize results list
results = []

# Fetch data for each player
for player in player_data:
    player_name = player["Player"]
    transfer_date = player["Transfer Date"]
    print(f"Fetching data for {player_name}, transfer date: {transfer_date}")

    # Example query to fetch player performance metrics (modify for the actual API being used)
    endpoint = f"{base_url}/players"
    params = {"search": player_name}

    try:
        # API request to fetch player data
        response = requests.get(endpoint, headers=headers, params=params)
        if response.status_code == 200:
            player_metrics = response.json()  # Parse JSON response

            # Append player-specific data
            results.append({
                "Player": player_name,
                "Transfer Date": transfer_date,
                "Performance Metrics": player_metrics  # Replace with relevant metrics fields
            })
        else:
            print(f"Error fetching data for {player_name}: {response.status_code} {response.text}")
            results.append({
                "Player": player_name,
                "Transfer Date": transfer_date,
                "Performance Metrics": "Error fetching data"
            })
    except Exception as e:
        print(f"Exception occurred for {player_name}: {e}")
        results.append({
            "Player": player_name,
            "Transfer Date": transfer_date,
            "Performance Metrics": "Exception occurred"
        })

# Display results
for result in results:
    print(result)

# (Optional) Save results to a CSV file
import pandas as pd

df = pd.DataFrame(results)
df.to_csv("player_metrics.csv", index=False)
