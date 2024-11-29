import pandas as pd
from arch import arch_model
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load stock data
stock_data = pd.read_csv('manu_stock_with_volatility.csv', parse_dates=['Date'])
stock_data['return'] = stock_data['Price'].pct_change().fillna(0)  # Calculate returns

# Rescale returns to avoid optimizer issues
stock_data['return'] *= 100

# Load transfer data and clean column names
data = pd.read_csv('transferETAV.csv', encoding='windows-1250')
data.columns = data.columns.str.strip()

# Select significant variables and merge
significant_vars = data[['SP_Surge', 'Overpayment Factor', 'Panic Buy Adjustment', 'Average Sentiment', 'PPD']]
stock_data = stock_data.reset_index(drop=True)
data = data.reset_index(drop=True)
stock_data = pd.concat([stock_data, data], axis=1)

# Train-test split
train_size = int(len(stock_data) * 0.7)
train_returns, test_returns = stock_data['return'][:train_size], stock_data['return'][train_size:]
train_significant_vars = significant_vars[:train_size]
test_significant_vars = significant_vars[train_size:]
# Align significant_vars with stock_data
aligned_significant_vars = pd.concat([significant_vars] * (len(stock_data) // len(significant_vars)), ignore_index=True)
aligned_significant_vars = aligned_significant_vars.iloc[:len(stock_data)]  # Ensure exact match
# Align significant_vars with stock_data by repeating or broadcasting
aligned_significant_vars = pd.concat([significant_vars] * (len(stock_data) // len(significant_vars)), ignore_index=True)
aligned_significant_vars = aligned_significant_vars.iloc[:len(stock_data)]  # Ensure exact match

# Split aligned significant_vars into training and testing sets
train_significant_vars = aligned_significant_vars[:train_size]
test_significant_vars = aligned_significant_vars[train_size:]

# Iterative one-step-ahead forecasting
forecasted_volatility = []
for i in range(len(test_returns)):
    # Use all available data up to the current test point
    temp_returns = pd.concat([train_returns, test_returns[:i + 1]], ignore_index=True)
    temp_significant_vars = pd.concat([train_significant_vars, test_significant_vars[:i + 1]], ignore_index=True)

    # Ensure alignment by matching lengths
    if len(temp_returns) != len(temp_significant_vars):
        print(f"Mismatch at iteration {i}: temp_returns={len(temp_returns)}, temp_significant_vars={len(temp_significant_vars)}")
        temp_significant_vars = temp_significant_vars.iloc[:len(temp_returns)]

    # Fit GARCH(1,1) model with significant variables in the mean equation
    model = arch_model(temp_returns, vol='Garch', mean='ARX', x=temp_significant_vars, p=1, q=1)
    fit = model.fit(disp='off')

    # Forecast one step ahead
    single_row_x = test_significant_vars.iloc[[i]]  # Extract a single row for forecasting
    single_row_x_dict = {
        "SP_Surge": single_row_x["SP_Surge"].values,
        "Overpayment Factor": single_row_x["Overpayment Factor"].values,
        "Panic Buy Adjustment": single_row_x["Panic Buy Adjustment"].values,
        "Average Sentiment": single_row_x["Average Sentiment"].values,
        "PPD": single_row_x["PPD"].values,
    }
    forecast = fit.forecast(horizon=1, x=single_row_x_dict)
    forecasted_volatility.append(np.sqrt(forecast.variance.values[-1, 0]))
# Compute actual volatility using rolling standard deviation
actual_volatility = test_returns.rolling(window=5).std().dropna()

# Align lengths
forecasted_volatility = forecasted_volatility[-len(actual_volatility):]

# Evaluate forecast
mae = mean_absolute_error(actual_volatility, forecasted_volatility)
rmse = mean_squared_error(actual_volatility, forecasted_volatility, squared=False)
print(f"MAE: {mae}, RMSE: {rmse}")

# Plot actual vs forecasted volatility
plt.figure(figsize=(12, 6))
aligned_dates = stock_data['Date'][actual_volatility.index]
plt.plot(aligned_dates, actual_volatility, label='Actual Volatility', color='blue')
plt.plot(aligned_dates, forecasted_volatility, label='Forecasted Volatility', color='orange')
plt.title('Actual vs Forecasted Volatility with Significant Variables (Iterative)', fontsize=14)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Volatility', fontsize=12)
plt.legend()
plt.grid(True)
plt.show()

# Save results to a CSV
forecast_df = pd.DataFrame({
    'Date': aligned_dates.values,
    'Actual_Volatility': actual_volatility.values,
    'Forecasted_Volatility': forecasted_volatility,
    'SP_Surge': test_significant_vars['SP_Surge'].iloc[-len(actual_volatility):].values,
    'Overpayment Factor': test_significant_vars['Overpayment Factor'].iloc[-len(actual_volatility):].values,
    'Panic Buy Adjustment': test_significant_vars['Panic Buy Adjustment'].iloc[-len(actual_volatility):].values,
    'Average Sentiment': test_significant_vars['Average Sentiment'].iloc[-len(actual_volatility):].values
})
forecast_df.to_csv('volatility_forecast_with_significant_vars_iterative.csv', index=False)
print("Results saved to volatility_forecast_with_significant_vars_iterative.csv")
