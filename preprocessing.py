import os
import pandas as pd

# Define the root directory where your nested folders are located
root_dir = r'C:\Users\KIIT\Downloads\data'

# Create an empty DataFrame to hold all CSV data
merged_df = pd.DataFrame()

# Walk through the directory and subdirectories
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        # Check if the file is a CSV
        if file.endswith('.csv'):
            file_path = os.path.join(subdir, file)
            # Read the CSV file
            df = pd.read_csv(file_path)
            # Append it to the merged DataFrame
            merged_df = pd.concat([merged_df, df], ignore_index=True)

# Save the merged DataFrame to an Excel file
merged_df.to_excel('merged_output.xlsx', index=False)
