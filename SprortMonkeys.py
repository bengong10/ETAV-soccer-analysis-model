import requests
import pandas as pd
import time

api_key = "wriZQIX5l2dMWjwtiJRGNtRSFbHWqQUo3OuuH43VjZ9ZZ3eZy7cXpJtcM6uA"
base_url = "https://soccer.sportmonks.com/api/v2.0"

man_united_team_id = 14  # Verified Manchester United team ID 
all_player_data = []

# Retrieve all seasons to map season names to IDs
seasons_response = requests.get(f"{base_url}/seasons?api_token={api_key}")
seasons_response.raise_for_status()
seasons_data = seasons_response.json().get('data', [])
season_name_to_id = {season['name']: season['id'] for season in seasons_data}

# Get all players for Manchester United
try:
    players_response = requests.get(
        f"{base_url}/teams/{man_united_team_id}?include=squad&api_token={api_key}"
    )
    players_response.raise_for_status()
    team_data = players_response.json().get('data', {})
    squad = team_data.get('squad', {}).get('data', [])

    # Loop over each player in the squad
    for player in squad:
        player_name = player.get("display_name")
        player_id = player.get("player_id")

        # 1. Determine relevant season IDs (current and previous seasons)
        relevant_seasons = [
            f"2022/2023",
            f"2023/2024"
        ]
        season_ids = [season_name_to_id[season] for season in relevant_seasons if season in season_name_to_id]

        # 2. Fetch season statistics for each relevant season
        for season_id in season_ids:
            season_stats_response = requests.get(
                f"{base_url}/players/{player_id}/season/{season_id}?api_token={api_key}"
            )
            season_stats_response.raise_for_status()
            season_data = season_stats_response.json().get('data', {})

            if season_data:  # Check if data exists for the season
                # Extract relevant stats
                stats = {
                    "Player": player_name,
                    "Season": season_data.get('season', {}).get('name', 'N/A'),
                    "Team": team_data.get('name', 'N/A'),
                    "Team ID": man_united_team_id,
                    "Appearances": season_data.get('appearances', 0),
                    "Goals": season_data.get('goals', 0),
                    "Assists": season_data.get('assists', 0),
                    # Add more stats if needed
                }
                all_player_data.append(stats)

            # Respect API rate limits
            time.sleep(1)

except requests.exceptions.RequestException as e:
    print(f"Error fetching data for Manchester United squad: {e}")
except (KeyError, IndexError) as e:
    print(f"Error parsing data for Manchester United squad: {e}")

# Create a Pandas DataFrame
df = pd.DataFrame(all_player_data)

# Save to Excel
df.to_excel("man_united_player_stats.xlsx", index=False)
print("Data saved to man_united_player_stats.xlsx")
