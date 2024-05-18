import os
import pandas as pd

# Directory containing the CSV files
data_dir = 'data/'

# List all files in the data directory
files = os.listdir(data_dir)

# Process each file that starts with "domain_comparison"
for file in files:
    if file.startswith("domain_comparison") and file.endswith(".csv"):
        print(f"Processing file: {file}")
        # Construct the full file path
        file_path = os.path.join(data_dir, file)
        
        # Read the CSV into a DataFrame
        df = pd.read_csv(file_path)
        
        # Remove the 'comparison' column if it exists
        if 'comparison' in df.columns:
            df.drop(columns=['comparison'], inplace=True)
        
        # Save the DataFrame back to a CSV file
        df.to_csv(file_path, index=False)

print("Processing complete.")
