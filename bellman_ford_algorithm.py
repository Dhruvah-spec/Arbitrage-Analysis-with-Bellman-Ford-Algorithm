## Runs the bellman-ford algorithm on the merged exchange rate data set at each time stamp.
## Identifies the most profitable arbitrage loop
## Determines profitability, currency loop and loop lenght for detected arbitrage opportunities

import pandas as pd
import numpy as np
import networkx as nx
import re

def get_canonical_form(cycle):
    """Standardizes the loop order for deduplication."""
    start_node = min(cycle)
    idx = cycle.index(start_node)
    return tuple(cycle[idx:] + cycle[:idx])

def parse_arbitrage(input_file, output_file):
    # Requirement: 5th decimal profit threshold (Multiplier > 1.00001)
    THRESHOLD = 1.00001 
    
    df = pd.read_excel(input_file)
    time_col = df.columns[0]
    
    final_results = []
    currency_counts = {}
    total_arbitrage_events = 0

    for index, row in df.iterrows():
        G = nx.DiGraph()
        timestamp = row[time_col]
        
        # 1. Build Graph with Strict 5-Decimal Rounding
        for col in df.columns:
            val = row[col]
            if not isinstance(val, (int, float)) or pd.isna(val) or val <= 0:
                continue
            
            rate = round(float(val), 5)
            pair_match = re.search(r"([A-Z]{3})-([A-Z]{3})", col)
            
            if pair_match:
                base, quote = pair_match.groups()
                if "Bid" in col:
                    G.add_edge(base, quote, rate=rate)
                elif "Ask" in col:
                    G.add_edge(quote, base, rate=rate)

        if len(G.nodes) < 2: continue

        # 2. Find All Simple Cycles
        candidate_loops = []
        try:
            for cycle in nx.simple_cycles(G):
                multiplier = 1.0
                for i in range(len(cycle)):
                    u = cycle[i]
                    v = cycle[(i + 1) % len(cycle)]
                    multiplier *= G[u][v]['rate']
                
                if multiplier >= THRESHOLD:
                    candidate_loops.append({
                        'canonical': get_canonical_form(cycle),
                        'profit_factor': multiplier,
                        'length': len(cycle)
                    })
            
            if candidate_loops:
                # 3. Selection Logic: Highest Profit Factor, then Shortest Length
                # Sort by profit factor DESC, then length ASC
                candidate_loops.sort(key=lambda x: (-x['profit_factor'], x['length']))
                
                best_loop = candidate_loops[0]
                total_arbitrage_events += 1
                
                # Record frequencies of each currency in the best loop
                for curr in best_loop['canonical']:
                    currency_counts[curr] = currency_counts.get(curr, 0) + 1
                
                path_str = " -> ".join(best_loop['canonical']) + f" -> {best_loop['canonical'][0]}"
                final_results.append({
                    'Timestamp': timestamp,
                    'Arbitrage_Loop': path_str,
                    'Profit_Factor': round(best_loop['profit_factor'], 8),
                    'Profit_%': round((best_loop['profit_factor'] - 1) * 100, 6),
                    'Path_Length': best_loop['length']
                })
                    
        except Exception:
            continue

    # 4. Prepare Frequency Statistics
    stats_data = []
    if total_arbitrage_events > 0:
        for curr, count in currency_counts.items():
            stats_data.append({
                'Currency': curr,
                'Frequency_%': round((count / total_arbitrage_events) * 100, 2)
            })
    
    # 5. Export to Excel with Multiple Sheets
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: Opportunities
        res_df = pd.DataFrame(final_results)
        res_df.to_excel(writer, sheet_name='Arbitrage Opportunities', index=False)
        
        # Sheet 2: Currency Analytics
        stats_df = pd.DataFrame(stats_data).sort_values(by='Frequency_%', ascending=False)
        stats_df.to_excel(writer, sheet_name='Currency Frequency', index=False)

    print(f"Analysis complete. Results saved to {output_file}")

parse_arbitrage()