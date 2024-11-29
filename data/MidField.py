import pandas as pd

# Load the dataset
file_path = 'All Manu players stats.xlsx'
data = pd.ExcelFile(file_path)

# Load the 'Midfield Actions' sheet
midfield_stats = data.parse('Passing')

# Display the columns to understand the structure
print(midfield_stats.columns)

# Define weights for each metric
metrics_weights = {
    'Assists': 0.2,
    'XA': 0.15,   # Expected Assists
    'Passing Completion %': 0.01,
    'Key Passes': 0.05,
    'XAG': 0.2   # Expected Assisted Goals
}

# Initialize a list to store midfielder performance data
midfielder_performance = []

# Iterate through each player to calculate metrics
for _, row in midfield_stats.iterrows():
    player_name = row.get('Player', 0)
    assists = row.get('Ast', 0)
    xa = row.get('xA', 0)
    passing_completion = row.get('Cmp%T', 0)
    key_passes = row.get('KP', 0)
    xag = row.get('xAG', 0)

    # Calculate weighted performance score
    score = (
        assists * metrics_weights['Assists'] +
        xa * metrics_weights['XA'] +
        passing_completion * metrics_weights['Passing Completion %'] +
        key_passes * metrics_weights['Key Passes'] +
        xag * metrics_weights['XAG']
    )

    # Append the calculated metrics to the list
    midfielder_performance.append({
        'Player': player_name,
        'Assists': assists,
        'XA': xa,
        'Passing Completion %': passing_completion,
        'Key Passes': key_passes,
        'XAG': xag,
        'Performance Score': score
    })

# Convert the list to a DataFrame for better visualization
midfielder_performance_df = pd.DataFrame(midfielder_performance)

# Define the output file path
output_file = 'midfielder_performance.xlsx'

# Save the DataFrame to an Excel file
midfielder_performance_df.to_excel(output_file, index=False)

print(f"Midfielder performance data has been saved to {output_file}")
