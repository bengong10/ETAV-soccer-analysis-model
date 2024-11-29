import pandas as pd

# Load stock data (replace 'stock_data.csv' with your actual file)
stock_data = pd.read_csv('manu_stock_with_volatility.csv', encoding='windows-1250')  # Specify detected encoding
stock_data['Date'] = pd.to_datetime(stock_data['Date'])  # Ensure Date column is in datetime format

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

# Convert transfer dates to datetime format
for player in player_data:
    player["Transfer Date"] = pd.to_datetime(player["Transfer Date"])

# Create a results list
results = []

# Loop through each player and find volatility on their transfer day
for player in player_data:
    transfer_date = player["Transfer Date"]
    player_name = player["Player"]

    # Try to find the volatility on the transfer date or next two days
    found = False
    for i in range(3):  # Check transfer day and the next 2 days
        check_date = transfer_date + pd.Timedelta(days=i)
        match = stock_data[stock_data['Date'] == check_date]
        if not match.empty:
            volatility = match['Volatility'].values[0]
            results.append({
                "Player": player_name,
                "Transfer Date": transfer_date.date(),
                "Closest Date": check_date.date(),
                "Volatility": volatility
            })
            found = True
            break

    # If no match is found within the range
    if not found:
        results.append({
            "Player": player_name,
            "Transfer Date": transfer_date.date(),
            "Closest Date": "Not Found",
            "Volatility": "Not Available"
        })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Display the results
print(results_df)

# Save to CSV
results_df.to_csv("transfer_day_volatility.csv", index=False)
