## Finds the reciprocal ask prices for each currency pair

import pandas as pd
from pathlib import Path
import sys


def process_file(input_path: Path, output_dir: Path):
    df = pd.read_excel(input_path)

    col = "Close(Ask)"
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in {input_path.name}. Available columns: {list(df.columns)}")

    df[f"Reciprocal_{col}"] = df[col].apply(lambda x: 1 / x if pd.notna(x) and x != 0 else None)

    output_path = output_dir / f"{input_path.stem}_processed{input_path.suffix}"
    df.to_excel(output_path, index=False)
    print(f"Saved: {output_path}")


def main():
    # --- CONFIGURE INPUT FILES HERE ---
    input_files = [
        
    ]

    # Auto-detect: if no files configured, look for .xlsx files in current directory
    if not input_files:
        input_files = sorted(Path(".").glob("*.xlsx"))
        if not input_files:
            print("No .xlsx files found. Please specify file paths in the script or place files in the current directory.")
            sys.exit(1)
        print(f"Auto-detected {len(input_files)} file(s): {[f.name for f in input_files]}")
    else:
        input_files = [Path(f) for f in input_files]

    if len(input_files) != 10:
        print(f"Warning: Expected 10 files, found {len(input_files)}. Continuing anyway.")

    output_dir = Path("processed_output")
    output_dir.mkdir(exist_ok=True)

    errors = []
    for file in input_files:
        try:
            process_file(Path(file), output_dir)
        except Exception as e:
            errors.append((file, str(e)))
            print(f"Error processing {file}: {e}")

    print(f"\nDone. {len(input_files) - len(errors)}/{len(input_files)} files processed successfully.")
    if errors:
        print("Failed files:")
        for f, err in errors:
            print(f"  {f}: {err}")


if __name__ == "__main__":
    main()