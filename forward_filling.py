## Fills in missing values exchange rate values from the dataset with the value in the timestamp just before it

import pandas as pd
import os

def process_manual_files(num_files=10):
    processed_count = 0
    
    while processed_count < num_files:
        print(f"\n--- File {processed_count + 1} of {num_files} ---")
        file_path = input("Enter the full path to the Excel file: ").strip()
        
        file_path = file_path.replace('"', '').replace("'", "")

        if not os.path.exists(file_path):
            print(f"Error: The file '{file_path}' was not found.")
            continue

        try:
            print("Reading file...")
            df = pd.read_excel(file_path)
            
            timestamp_col = df.columns[0]
            
            # 1. Convert to datetime and strip timezone info immediately
            # .dt.tz_localize(None) makes it 'timezone unaware'
            df[timestamp_col] = pd.to_datetime(df[timestamp_col]).dt.tz_localize(None)
            
            # 2. Set index and reindex
            df.set_index(timestamp_col, inplace=True)
            full_range = pd.date_range(start=df.index.min(), 
                                       end=df.index.max(), 
                                       freq='S')
            
            # 3. Reindex and Forward Fill
            df_filled = df.reindex(full_range).ffill()
            
            # 4. Format for output
            df_filled.index.name = timestamp_col
            df_filled.reset_index(inplace=True)

            # 5. Save the output
            dir_name = os.path.dirname(file_path)
            base_name = os.path.basename(file_path)
            output_path = os.path.join(dir_name, f"filled_{base_name}")
            
            df_filled.to_excel(output_path, index=False)
            print(f"Success! Saved to: {output_path}")
            
            processed_count += 1

        except Exception as e:
            print(f"An error occurred while processing this file: {e}")

if __name__ == "__main__":
    process_manual_files(10)