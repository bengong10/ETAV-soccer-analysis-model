import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Create the player data
data = {
    'Sale Price (£M)': [73.00, 40.00, 13.00, 85.50, 60.00, 13.50, 55.00, 0.00, 55.00, 47.20, 72.00],
    'Market Value (£M)': [33.00, 0.00, 0.00, 25.00, 20.00, 18.00, 50.00, 8.00, 35.00, 35.00, 65.00],
    'Performance (Rating out of 10)': [6.5, 7.0, 8.0, 6.0, 7.5, 7.0, 7.5, 7.0, 7.0, 7.0, 7.5],
    'Panic Sale Adjustment': [0.71, 0.50, 0.042, 0.033, 0.16, 0.30, 0.18, 0.28, 0.088, 0.10, 0.12],
    'Post-Performance Drop': [-35.0, -30.0, -25.0, -40.0, -8.0, -5.0, -3.0, -10.0, -12.0, -8.0, -6.0],
    'ETAV': [4.5, 3.8, 2.8, 6.0, 4.8, 3.3, 4.1, 2.3, 4.6, 4.2, 3.9]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define independent variables (features) and the dependent variable (target)
X = df[['Sale Price (£M)', 'Market Value (£M)', 'Performance (Rating out of 10)', 'Panic Sale Adjustment', 'Post-Performance Drop']]
y = df['ETAV']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the Linear Regression model
model = LinearRegression()

# Fit the model on the training data
model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Calculate the performance of the model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Display the results
coefficients = pd.DataFrame(model.coef_, X.columns, columns=['Coefficient'])
print("Coefficients:\n", coefficients)
print("\nIntercept:", model.intercept_)
print("\nMean Squared Error (MSE):", mse)
print("\nR-squared (R2):", r2)

# Display predictions alongside actual ETAV values
results = pd.DataFrame({'Actual ETAV': y_test, 'Predicted ETAV': y_pred})
print("\nResults:\n", results)
