import pandas as pd
from arch import arch_model
import matplotlib.pyplot as plt


# Load stock price data
stock_data = pd.read_csv('manuStock.csv', encoding='windows-1250')  # Specify detected encoding

# Load ETAV data
etav_data = pd.read_csv('ETAV.csv', encoding='windows-1250')  

# Ensure consistent date format
stock_data['Date'] = pd.to_datetime(stock_data['Date'], format='%d-%b-%y', errors='coerce')
etav_data['Date'] = pd.to_datetime(etav_data['Date'], format='%d-%b-%y', errors='coerce')

# Merge datasets on Date
data = pd.merge(stock_data, etav_data, on='Date', how='inner')

# Check if 'EVAV' exists in the merged DataFrame
print("Columns in merged DataFrame:", data.columns)
if 'ETAV' not in data.columns:
    raise ValueError("The 'ETAV' column is missing in the merged DataFrame. Check column names or merge logic.")

# Prepare returns and ETAV
data['return'] = data['Price'].pct_change().dropna() * 100  # Scale returns for GARCH
etav = data['ETAV']

# Fit GARCH(1,1) model with EVAV in the variance equation
model = arch_model(data['return'].dropna(), vol='Garch', p=1, q=1, mean='constant', x=etav)
garch_fit = model.fit(disp='off')

# Print summary
print(garch_fit.summary())

# Align the Date column with the volatility data
aligned_dates = data['Date'][1:]  # Drop the first date to match the length of conditional_volatility

# Plot the conditional volatility
plt.figure(figsize=(12, 6))
plt.plot(aligned_dates, garch_fit.conditional_volatility, label='Volatility', color='blue')
plt.title('Manchester United Stock Volatility Trends Over Time', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Volatility', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()
