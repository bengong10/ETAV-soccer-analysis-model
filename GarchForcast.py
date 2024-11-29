import pandas as pd
from arch import arch_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load stock price data
stock_data = pd.read_csv('manuStock.csv')  

# Ensure 'Price' column exists and handle missing values
stock_data['Price'] = stock_data['Price'].fillna(method='ffill')

# Calculate daily returns
stock_data['return'] = stock_data['Price'].pct_change()

# Drop NaN values from the return series
returns = stock_data['return'].dropna()

# Rescale returns for better convergence
scaled_returns = returns * 100

# Fit a GARCH(1,1) model
model = arch_model(scaled_returns, vol='Garch', p=1, q=1)
garch_fit = model.fit(disp='off')  # Suppress fitting output

# Get conditional volatility
stock_data = stock_data.dropna()  # Align data after dropping NaNs in returns
stock_data['Volatility'] = garch_fit.conditional_volatility / 100  # Rescale back

# Save the stock_data DataFrame with Volatility to a new CSV file
output_file = 'manu_stock_with_volatility.csv'
stock_data.to_csv(output_file, index=False)
print(f"Output with volatility added has been saved to {output_file}")

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

# Out-of-Sample Testing
train_size = int(len(returns) * 0.7)
train, test = scaled_returns[:train_size], scaled_returns[train_size:]

# Fit GARCH(1,1) on training data
model = arch_model(train, vol='Garch', p=1, q=1)
fit = model.fit(disp='off')

# Forecast on test data
forecast = fit.forecast(horizon=len(test))
forecast_volatility = forecast.variance.iloc[-len(test):].values.flatten() ** 0.5 / 100  # Rescale back

# Calculate actual realized volatility from the test data
actual_volatility = test.rolling(window=5).std().iloc[-len(forecast_volatility):].values

# Align lengths by dropping NaNs
valid_indices = ~pd.isna(actual_volatility)
actual_volatility = actual_volatility[valid_indices]
forecast_volatility = forecast_volatility[valid_indices]

# Plot Forecasted vs Actual Volatility
plt.figure(figsize=(12, 6))
plt.plot(forecast_volatility, label='Forecasted Volatility', linestyle='--', color='orange')
plt.plot(actual_volatility, label='Actual Volatility', color='blue')
plt.title('Forecasted vs Actual Volatility', fontsize=14)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Volatility', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# Evaluate Forecast Accuracy
mae = mean_absolute_error(actual_volatility, forecast_volatility)
rmse = mean_squared_error(actual_volatility, forecast_volatility, squared=False)
print(f"Forecast Accuracy Metrics:\nMAE: {mae:.4f}\nRMSE: {rmse:.4f}")
