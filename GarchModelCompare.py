import pandas as pd
from arch import arch_model
import numpy as np
import matplotlib.pyplot as plt


# Load stock price data
stock_data = pd.read_csv('manuStock.csv') 
stock_data['return'] = stock_data['Price'].pct_change().dropna()

# Define a function to fit and evaluate different GARCH models
def fit_garch_models(returns):
    models = {
        'GARCH(1,1)': arch_model(returns, vol='Garch', p=1, q=1),
        'GARCH(2,1)': arch_model(returns, vol='Garch', p=2, q=1),
        'EGARCH(1,1)': arch_model(returns, vol='EGarch', p=1, q=1),
        'GJR-GARCH(1,1)': arch_model(returns, vol='GARCH', p=1, q=1, o=1)
    }

    results = {}
    for model_name, model in models.items():
        fit = model.fit(disp='off')
        results[model_name] = {
            'AIC': fit.aic,
            'BIC': fit.bic,
            'Log-Likelihood': fit.loglikelihood,
            'Model': fit
        }

    return results


# Fit models and collect results
returns = stock_data['return'].dropna()
garch_results = fit_garch_models(returns*100)

# Display the results for comparison
for model_name, result in garch_results.items():
    print(
        f"{model_name} -> AIC: {result['AIC']:.2f}, BIC: {result['BIC']:.2f}, Log-Likelihood: {result['Log-Likelihood']:.2f}")

# Fit a GARCH(1,1) model
model = arch_model(returns*100, vol='Garch', p=1, q=1)
garch_fit = model.fit(disp='off')  # Suppress fitting output
forecast = garch_fit.forecast(horizon=100)  # Example: 10-day volatility forecast
print(forecast.variance[-1:])
forecasted_volatilities = np.sqrt(forecast.variance)
forecasted_volatilities.to_csv('forecasted_volatilities.csv', index=False)

# Print volatilities
print("Forecasted Volatilities:", forecasted_volatilities)

plt.figure(figsize=(12, 6))
plt.plot(forecasted_volatilities.iloc[0].values, label='Forecasted Volatility')
plt.title('Forecasted Volatility Over 100 Days')
plt.xlabel('Day')
plt.ylabel('Volatility')
plt.legend()
plt.grid(True)
plt.show()
