import pandas as pd
import statsmodels.api as sm

# Create the dataset based on the provided table
data = pd.read_csv('post_season_PPD_Sentiment_volatility.csv', encoding='windows-1250')  # Specify detected encoding
df = pd.DataFrame(data)


# Independent variables
X = df[["PPD", "Average Sentiment"]]

# Dependent variable
y = df["Average Volatility"]

# Add a constant for the regression intercept
X = sm.add_constant(X)

# Perform the regression
model = sm.OLS(y, X).fit()

# Display the regression summary
print(model.summary())

# Save the results to a file
with open("ppd_sentiment_volatility_regression_results.txt", "w") as file:
    file.write(model.summary().as_text())

# Print the regression equation
coefficients = model.params
equation = f"Average Volatility = {coefficients['const']:.5f} + ({coefficients['PPD']:.5f} * PPD) + " \
           f"({coefficients['Average Sentiment']:.5f} * Average Sentiment)"
print("\nRegression Equation:")
print(equation)
