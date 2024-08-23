import pandas as pd

# Convert the string data into a pandas DataFrame
csv_path = '../aug22_data/eusd_pricepeg.csv'
eusd_pricepeg_df = pd.read_csv(csv_path)

# # Convert the 'hour' column to datetime
eusd_pricepeg_df['hour'] = pd.to_datetime(eusd_pricepeg_df['hour'])

# # Set the 'hour' column as the index
eusd_pricepeg_df.set_index('hour', inplace=True)

# # Resample the data by month and calculate the mean for each network
monthly_avg_df = eusd_pricepeg_df.resample('M').mean()

# # Rename the columns to match the desired output
monthly_avg_df.columns = ['Mainnet', 'Base', 'Arbitrum']

# # Convert the index to month names
monthly_avg_df.index = monthly_avg_df.index.strftime('%B')
# # Display the DataFrame


# Calculate the average for each column
average_row = monthly_avg_df.mean().to_frame().T

# Rename the index of the average row to "Average"
average_row.index = ['Average']

# Append the average row to the DataFrame
monthly_avg_df_with_avg = pd.concat([monthly_avg_df, average_row])
monthly_avg_df_with_avg.index.name = "Date"

print(monthly_avg_df_with_avg)