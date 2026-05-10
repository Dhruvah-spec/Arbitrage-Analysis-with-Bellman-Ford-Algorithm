## Reads the arbitrage results file and counts the occurrences of each unique loop.

import pandas as pd

def count_arbitrage_loops(input_file, output_file):
    """
    Reads the arbitrage results file and counts the occurrences of each unique loop.
    """
    try:
        # Load the results from the previous script
        df = pd.read_excel(input_file)
        
        if 'Arbitrage_Loop' not in df.columns:
            print("Error: Could not find 'Arbitrage_Loop' column in the input file.")
            return

        # 1. Count occurrences of each unique loop
        # We use value_counts() which returns a Series of counts
        loop_counts = df['Arbitrage_Loop'].value_counts().reset_index()
        
        # Rename columns for clarity
        loop_counts.columns = ['Arbitrage_Loop', 'Occurrence_Count']
        
        # 2. Calculate the percentage of total arbitrage events
        total_events = len(df)
        loop_counts['Frequency_%'] = round((loop_counts['Occurrence_Count'] / total_events) * 100, 2)

        # 3. Save the summary to a new Excel file
        loop_counts.to_excel(output_file, index=False)
        
        print(f"Loop analysis complete.")
        print(f"Total arbitrage opportunities analyzed: {total_events}")
        print(f"Summary saved to: {output_file}")
        
        # Display the top 5 most frequent loops in the console
        print("\nTop 5 Most Frequent Loops:")
        print(loop_counts.head(5).to_string(index=False))

    except Exception as e:
        print(f"An error occurred: {e}")

# Usage:
count_arbitrage_loops()