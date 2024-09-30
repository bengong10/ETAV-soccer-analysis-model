import pandas as pd

# Create the player data (price is from tranfermarkt)
data = {
    'Player': ['Jadon Sancho', 'Raphaël Varane', 'Cristiano Ronaldo', 'Antony', 'Casemiro', 'Tyrell Malacia',
               'Lisandro Martínez', 'Christian Eriksen', 'Mason Mount', 'André Onana', 'Rasmus Højlund'],
    'Sale Price (£M)': [73.00, 40.00, 13.00, 85.50, 60.00, 13.50, 55.00, 0.00, 55.00, 47.20, 72.00],
    'Market Value (£M)': [33.00, 0.00, 0.00, 25.00, 20.00, 18.00, 50.00, 8.00, 35.00, 35.00, 65.00],
    'Performance (Rating out of 10)': [6.5, 7.0, 8.0, 6.0, 7.5, 7.0, 7.5, 7.0, 7.0, 7.0, 7.5],
    'Days Left in Transfer Window': [60, 35, 4, 3, 12, 18, 12, 14, 7, 8, 10],
    'Media Coverage Intensity': [85, 70, 95, 90, 75, 60, 65, 50, 80, 77, 82],
    'Initial Surge (%)': [4.0, 3.5, 5.0, 5.5, 4.2, 3.0, 3.8, 2.5, 4.5, 4.0, 3.8],
    'Club Value Change (%) after Performance': [-15, -10, -25, -20, -12, -8, -5, -10, -12, -8, -6]
}

# Create DataFrame
df = pd.DataFrame(data)

# Calculate Undervaluation Factor
df['Undervaluation Factor'] = df['Sale Price (£M)'] / df['Market Value (£M)'].replace(0, float('inf'))

# Calculate Panic Sale Adjustment
df['Panic Sale Adjustment'] = df['Days Left in Transfer Window'] / df['Media Coverage Intensity']

# Calculate Post-Performance Drop
df['Post-Performance Drop'] = df['Initial Surge (%)'] - (df['Performance (Rating out of 10)'] / 10) * 100

# Calculate ETAV without GARCH Volatility
df['ETAV'] = df['Initial Surge (%)'] + 0.5 * df['Undervaluation Factor'] + 0.3 * df['Panic Sale Adjustment'] + df['Post-Performance Drop']

# Display final DataFrame
print(df[['Player', 'Sale Price (£M)', 'Market Value (£M)', 'Performance (Rating out of 10)',
          'Undervaluation Factor', 'Panic Sale Adjustment', 'Post-Performance Drop', 'ETAV']])
