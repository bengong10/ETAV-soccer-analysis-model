import pandas as pd

# Load the dataset
file_path = 'All Manu players stats.xlsx'
data = pd.ExcelFile(file_path)

# Load the 'Goalkeeping' sheet
goalkeeping_stats = data.parse('AdvancedGoalKeeping')

# Define weights for each metric
metrics_weights = {
    'GA90': -0.1,   # own Goals Allowed
 #   'PSxG+/-': 1.5,    #post shot expect gola - goal allowed
    '/90': 1,   # above average saving ability
    'Save%': 0.016  # Save Percentage
}

# Initialize a list to store goalkeeper performance data
goalkeeper_performance = []

# Iterate through each player to calculate metrics
for _, row in goalkeeping_stats.iterrows():
    player_name = row.get('Player', 'Unknown')
    goals_allowed_90 = row.get('GA90', 0)
    PSXG_GA90 = row.get('/90', 0)
    save_percentage = row.get('Save%', 0)

    # Calculate weighted performance score
    score = (
        goals_allowed_90 * metrics_weights['GA90'] +
        PSXG_GA90 * metrics_weights['/90'] +
        save_percentage * metrics_weights['Save%']
    )

    # Append the calculated metrics to the list
    goalkeeper_performance.append({
        'Player': player_name,
        'Goals Allowed /90': goals_allowed_90,
        'PSXG_GA90': PSXG_GA90,
        'Save Percentage': save_percentage,
        'Performance Score': score
    })

# Convert the list to a DataFrame for better visualization
goalkeeper_performance_df = pd.DataFrame(goalkeeper_performance)

# Define the output file path
output_file = 'goalkeeper_performance.xlsx'

# Save the DataFrame to an Excel file
goalkeeper_performance_df.to_excel(output_file, index=False)

print(f"Goalkeeper performance data has been saved to {output_file}")
