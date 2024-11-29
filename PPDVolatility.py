import pandas as pd

# Load stock data
stock_data = pd.read_csv('manu_stock_with_volatility.csv', encoding='windows-1250')
stock_data['Date'] = pd.to_datetime(stock_data['Date'])

# Players and their transfer and season end dates
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

# Convert transfer and season end dates to datetime
for player in player_data:
    player["Transfer Date"] = pd.to_datetime(player["Transfer Date"])
    player["Season End Date"] = pd.to_datetime(player["Season End Date"])

# Calculate average volatility for each player
results = []
for player in player_data:
    transfer_date = player["Transfer Date"]
    season_end_date = player["Season End Date"]
    player_name = player["Player"]

    # Filter stock data for the period from transfer date to season end date
    period_data = stock_data[(stock_data['Date'] >= transfer_date) & (stock_data['Date'] <= season_end_date)]

    if not period_data.empty:
        average_volatility = period_data['Volatility'].mean()
    else:
        average_volatility = None

    results.append({
        "Player": player_name,
        "Transfer Date": transfer_date.date(),
        "Season End Date": season_end_date.date(),
        "Average Volatility": average_volatility
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save results to CSV
results_file = "average_volatility_per_player.csv"
results_df.to_csv(results_file, index=False)
