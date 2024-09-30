import pandas as pd
import numpy as np
from arch import arch_model
from sklearn.linear_model import LinearRegression

# Sample stock price data 
stock_prices = pd.Series([15.20, 15.25, 15.30, 15.10, 15.15, 15.05, 15.00, 14.95, 14.90, 14.85, 14.80])

# Calculate daily returns
returns = 100 * stock_prices.pct_change().dropna()

# Fit a GARCH(1,1) model to the returns
model_garch = arch_model(returns, vol='Garch', p=1, q=1)
garch_fit = model_garch.fit(disp='off')

# Extract the conditional volatility from GARCH model
volatility = garch_fit.conditional_volatility

# Ensure that the number of volatility values matches the number of players
# Truncate to match player data size
volatility = volatility[-11:]

# Player data
data = {
    'Player': ['Jadon Sancho', 'Raphaël Varane', 'Cristiano Ronaldo', 'Antony', 'Casemiro', 'Tyrell Malacia',
               'Lisandro Martínez', 'Christian Eriksen', 'Mason Mount', 'André Onana', 'Rasmus Højlund'],
    'Sale Price (£M)': [73.0, 40.0, 13.0, 85.5, 60.0, 13.5, 55.0, 0.0, 55.0, 47.2, 72.0],
    'Market Value (£M)': [33, 0, 0, 25, 20, 8, 50, 8, 35, 35, 65],
    'Performance (Rating out of 10)': [6.5, 7.0, 8.0, 6.0, 7.5, 7.0, 7.5, 7.0, 7.0, 7.0, 7.5],
    'Days Left in Transfer Window': [60, 35, 4, 3, 12, 18, 12, 14, 7, 7, 10],
    'Media Coverage Intensity': [85, 70, 95, 90, 75, 60, 65, 50, 80, 77, 82],
    'Initial Surge (%)': [4.0, 3.5, 5.0, 5.5, 4.2, 3.0, 3.8, 2.5, 4.5, 4.0, 3.8],
    'Club Value Change (%) after Performance': [-15, -10, -25, -20, -12, -8, -5, -10, -12, -8, -6],
    'Undervaluation Factor': [2.21, None, None, 3.42, 3.0, 0.75, 1.1, None, 1.57, 1.35, 1.11],
    'Panic Sale Adjustment': [0.71, 0.5, 0.042, 0.033, 0.16, 0.3, 0.18, 0.28, 0.088, 0.1, 0.12],
    'Post-Performance Drop': [-1.5, -2.0, -3.0, -2.5, -1.8, -0.5, -0.8, -1.0, -1.0, -1.5, -1.0],
    'ETAV': [4.5, 3.8, 2.8, 6.0, 4.8, 4.3, 4.1, 2.3, 4.6, 4.2, 3.9]
}

# Create DataFrame and add GARCH Volatility
df = pd.DataFrame(data)

# Truncate player data to match volatility data size
df = df.iloc[-len(volatility):]

# Assign the volatility values
df['Volatility'] = volatility.values 

# Drop rows where Market Value is zero or NaN in Undervaluation Factor
df['Undervaluation Factor'] = df['Undervaluation Factor'].replace({None: 0, float('nan'): 0})
df['Undervaluation Factor'] = df['Sale Price (£M)'] / df['Market Value (£M)'].replace(0, float('nan'))

# Drop rows where Undervaluation Factor is NaN due to Market Value being zero
df.dropna(subset=['Undervaluation Factor'], inplace=True)

# Define independent variables (features) and dependent variable (target)
X = df[['Undervaluation Factor', 'Panic Sale Adjustment', 'Post-Performance Drop', 'Volatility']]
y = df['ETAV']

# Initialize Linear Regression Model
model = LinearRegression()

# Fit the model
model.fit(X, y)

# Get the weight factors
coefficients = pd.DataFrame(model.coef_, X.columns, columns=['Weight Factor'])
intercept = model.intercept_

# Display the weight factors and intercept
print("Weight Factors (β, γ, δ, Φ):\n", coefficients)
print("\nIntercept (constant):", intercept)

# Update ETAV Calculation using the formula
df['Predicted ETAV'] = intercept + df['Undervaluation Factor'] * coefficients.loc['Undervaluation Factor', 'Weight Factor'] + \
                        df['Panic Sale Adjustment'] * coefficients.loc['Panic Sale Adjustment', 'Weight Factor'] + \
                        df['Post-Performance Drop'] * coefficients.loc['Post-Performance Drop', 'Weight Factor'] + \
                        df['Volatility'] * coefficients.loc['Volatility', 'Weight Factor']

# Display the DataFrame with original and predicted ETAV values
print(df[['Player', 'Sale Price (£M)', 'Market Value (£M)', 'Undervaluation Factor',
          'Panic Sale Adjustment', 'Post-Performance Drop', 'Volatility', 'ETAV', 'Predicted ETAV']])
