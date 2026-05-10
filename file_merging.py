## Merges all currency pair files into one sheet

import re
import sys
from pathlib import Path
from functools import reduce

import pandas as pd


def extract_pair(filename: str) -> str:
    """Extract currency pair (e.g. CNH-JPY) from filename."""
    stem = Path(filename).stem
    match = re.search(r'[A-Z]{3}[-_][A-Z]{3}', stem, re.IGNORECASE)
    if match:
        return match.group(0).upper().replace("_", "-")
    # Fallback: use full stem if no pair pattern found
    return stem


def load_file(path: Path) -> pd.DataFrame:
    pair = extract_pair(path.name)

    df = pd.read_excel(path)

    missing = [c for c in ("UTC", "Close(Bid)", "Reciprocal_Close(Ask)") if c not in df.columns]
    if missing:
        raise ValueError(f"{path.name}: missing columns {missing}. Found: {list(df.columns)}")

    return df[["UTC", "Close(Bid)", "Reciprocal_Close(Ask)"]].rename(columns={
        "Close(Bid)": f"Close(Bid)_{pair}",
        "Reciprocal_Close(Ask)": f"Reciprocal_Close(Ask)_{pair}",
    })


def main():
    # --- CONFIGURE INPUT FILES HERE ---
    input_files = [
    
    ]

    # Auto-detect: scan processed_output/ then current directory
    if not input_files:
        for search_dir in (Path("processed_output"), Path(".")):
            found = sorted(search_dir.glob("*.xlsx"))
            if found:
                input_files = found
                print(f"Auto-detected {len(input_files)} file(s) from '{search_dir}/'")
                break

    if not input_files:
        print("No .xlsx files found. Specify paths in input_files or place files in processed_output/.")
        sys.exit(1)

    input_files = [Path(f) for f in input_files]

    if len(input_files) != 10:
        print(f"Warning: Expected 10 files, found {len(input_files)}. Continuing anyway.")

    dfs = []
    for path in input_files:
        try:
            dfs.append(load_file(path))
            print(f"Loaded: {path.name}  →  pair: {extract_pair(path.name)}")
        except Exception as e:
            print(f"ERROR – {path.name}: {e}")
            sys.exit(1)

    merged = reduce(lambda left, right: pd.merge(left, right, on="UTC", how="outer"), dfs)
    merged.sort_values("UTC", inplace=True)
    merged.reset_index(drop=True, inplace=True)

    output_path = Path()
    merged.to_excel(output_path, index=False)
    print(f"\nMerged file saved → {output_path}  ({len(merged)} rows, {len(merged.columns)} columns)")


if __name__ == "__main__":
    main()