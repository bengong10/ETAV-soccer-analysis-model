import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Create the dataset based on the provided table
data = pd.read_csv('transferETAV.csv', encoding='windows-1250')  # Specify detected encoding
df = pd.DataFrame(data)

# Independent variables
X = df[["SP_Surge", "Overpayment Factor", "Panic Buy Adjustment", "Average Sentiment"]]

# Dependent variable
y = df["Volatility"]

# Add a constant for the regression intercept
X = sm.add_constant(X)

# Perform the regression
model = sm.OLS(y, X).fit()

# Display the regression summary
print(model.summary())

# Save the results to a file
with open("regression_results.txt", "w") as file:
    file.write(model.summary().as_text())
# Print the regression equation
coefficients = model.params
equation = f"Volatility = {coefficients['const']:.5f} + ({coefficients['Overpayment Factor']:.5f} * Overpayment Factor) + " \
           f"({coefficients['Panic Buy Adjustment']:.5f} * Panic Buy Adjustment) + " \
           f"({coefficients['Average Sentiment']:.5f} * Average Sentiment)"
print("\nRegression Equation:")
print(equation)