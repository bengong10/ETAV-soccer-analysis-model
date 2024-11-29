import pandas as pd
import matplotlib.pyplot as plt
from arch import arch_model

# Load stock data
stock_data = pd.read_csv("manu_stock_with_volatility.csv")
stock_data['Date'] = pd.to_datetime(stock_data['Date'])

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

# GARCH Volatility Analysis
returns = stock_data['Price'].pct_change().dropna()
model = arch_model(returns, vol='Garch', p=1, q=1)
garch_fit = model.fit(disp="off")
volatility = garch_fit.conditional_volatility

# Plot combined stock price and volatility trend with transfer dates
plt.figure(figsize=(14, 7))

# Stock price trend
plt.plot(stock_data['Date'], stock_data['Price'], label='Stock Price', color='blue', linewidth=1.5)

# Volatility trend
#plt.plot(stock_data['Date'][1:], volatility, label='GARCH Volatility', color='green', linewidth=1.5)

# Highlight transfer dates
for player in player_data:
    transfer_date = player["Transfer Date"]
    player_name = player["Player"]
    plt.axvline(x=transfer_date, linestyle='--', color='red', alpha=0.7)
    plt.text(transfer_date, stock_data['Price'].max(), player_name, rotation=90, verticalalignment='top', fontsize=8)

# Chart formatting
plt.title("MANU Stock Trends with Player Transfer Dates", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Stock Price", fontsize=12)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
