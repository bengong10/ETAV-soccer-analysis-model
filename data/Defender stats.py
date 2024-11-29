import pandas as pd

# Load the dataset
file_path = 'All Manu players stats.xlsx'
data = pd.ExcelFile(file_path)

# Load the 'Defensive Actions' sheet
defensive_stats = data.parse('Defensive Actions')

# Display the columns to understand the structure
print(defensive_stats.columns)

# Define weights for each metric
metrics_weights = {
    'Tackles': 0.015,
    'Tkl+Int': 0.014,  # Tackles + Interceptions
    'Tkl%': 0.001,     # Tackle Percentage
    'Blocks': 0.014,
    'Errors': -0.03   # Negative weight for errors
}

# Initialize a list to store defender performance data
defender_performance = []

# Iterate through each player to calculate metrics
for _, row in defensive_stats.iterrows():
    player_name = row.get('Player', 'Unknown')
    tackles = row.get('Tkl', 0)
    interceptions = row.get('Int', 0)
    tackle_percentage = row.get('Tkl%', 0)
    blocks = row.get('Blocks', 0)
    errors = row.get('Err', 0)

    # Calculate Tackles + Interceptions
    tkl_int = tackles + interceptions

    # Calculate weighted performance score
    score = (
        tackles * metrics_weights['Tackles'] +
        tkl_int * metrics_weights['Tkl+Int'] +
        tackle_percentage * metrics_weights['Tkl%'] +
        blocks * metrics_weights['Blocks'] +
        errors * metrics_weights['Errors']
    )

    # Append the calculated metrics to the list
    defender_performance.append({
        'Player': player_name,
        'Tackles': tackles,
        'Interceptions': interceptions,
        'Tkl+Int': tkl_int,
        'Tackle Percentage': tackle_percentage,
        'Blocks': blocks,
        'Errors': errors,
        'Performance Score': score
    })

# Convert the list to a DataFrame for better visualization
defender_performance_df = pd.DataFrame(defender_performance)

# Define the output file path
output_file = 'defender_performance.xlsx'

# Save the DataFrame to an Excel file
defender_performance_df.to_excel(output_file, index=False)

print(f"Defender performance data has been saved to {output_file}")
