import pandas as pd

# Load the dataset
file_path = 'All Manu players stats.xlsx'
data = pd.ExcelFile(file_path)

# Load the 'Offensive Actions' sheet
offensive_stats = data.parse('Shooting')

# Display the columns to understand the structure
print(offensive_stats.columns)

# Define weights for each metric
metrics_weights = {
    'SoT%': 2,    # shot on target
    'G/Sh': 3,    #Goal per shot
    'npxG/Sh': 4,   # non penalty Goals per shot
    'np:G-xG': 1.1,   # non penalty goals minus expected goals
}

# Initialize a list to store forward performance data
forward_performance = []

# Iterate through each player to calculate metrics
for _, row in offensive_stats.iterrows():
    player_name = row.get('Player', 0)
    SOT = row.get('SoT%', 0)
    GlPerSh = row.get('G/Sh', 0)
    npxGPerSh = row.get('npxG/Sh', 0)
    npg_XG = row.get('np:G-xG', 0)
    goals = row.get('Gls', 0)

    if goals==0:
        goals=1
    # Calculate weighted performance score
    score = (
        SOT * metrics_weights['SoT%'] /100+
        GlPerSh * metrics_weights['G/Sh'] +
        npxGPerSh * metrics_weights['npxG/Sh'] +
        npg_XG * metrics_weights['np:G-xG']/goals
    )

    # Append the calculated metrics to the list
    forward_performance.append({
        'Player': player_name,
        'SOT%': SOT,
        'G/Sh': GlPerSh,
        'npxG/Sh': npxGPerSh,
        'np:G-xG': npg_XG,
        'Performance Score': score
    })

# Convert the list to a DataFrame for better visualization
forward_performance_df = pd.DataFrame(forward_performance)

# Define the output file path
output_file = 'forward_performance.xlsx'

# Save the DataFrame to an Excel file
forward_performance_df.to_excel(output_file, index=False)

print(f"Forward performance data has been saved to {output_file}")
