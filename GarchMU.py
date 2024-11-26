import pandas as pd
from arch import arch_model
import matplotlib.pyplot as plt


# Load stock price data
stock_data = pd.read_csv('manuStock.csv')  # Replace with your file path

# Ensure 'Price' column exists and handle missing values
stock_data['Price'] = stock_data['Price'].fillna(method='ffill')

# Calculate daily returns
stock_data['return'] = stock_data['Price'].pct_change()

# Drop NaN values from the return series
returns = stock_data['return'].dropna()

# Fit a GARCH(1,1) model
model = arch_model(returns, vol='Garch', p=1, q=1)
garch_fit = model.fit(disp='off')  # Suppress fitting output

# Get conditional volatility
stock_data = stock_data.dropna()  # Align data after dropping NaNs in returns
stock_data['Volatility'] = garch_fit.conditional_volatility

# Print relevant columns
print(stock_data[['Date', 'Price', 'return', 'Volatility']])
# Save the stock_data DataFrame with Volatility to a new CSV file
#output_file = 'manu_stock_with_volatility.csv'
#stock_data.to_csv(output_file, index=False)

#print(f"Output with volatility added has been saved to {output_file}")


# Ensure the 'Date' column is in datetime format for plotting
stock_data['Date'] = pd.to_datetime(stock_data['Date'])

# Plot Volatility Trends
plt.figure(figsize=(12, 6))
plt.plot(stock_data['Date'], stock_data['Volatility'], label='Volatility', color='blue')
plt.title('Manchester United Stock Volatility Trends Over Time', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Volatility', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# Example of out-of-sample testing
train_size = int(len(returns) * 0.7)
train, test = returns[:train_size], returns[train_size:]

# Fit GARCH(1,1) on training data
model = arch_model(train, vol='Garch', p=1, q=1)
fit = model.fit(disp='off')

# Forecast on test data
forecast = fit.forecast(horizon=len(test))
forecast_volatility = forecast.variance[-1:] ** 0.5

# Compare predicted volatility to actual
actual_volatility = test.rolling(window=5).std()  # Example of realized volatility

