from pathlib import Path
import duckdb

# -----------------------------
# 1. Set up folder paths
# -----------------------------
# Find the project root (one level above src)
project_root = Path(__file__).resolve().parent.parent

raw_dir = project_root / "data" / "raw"
cleaned_dir = project_root / "data" / "cleaned"

cleaned_dir.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 2. Connect to DuckDB
# -----------------------------
con = duckdb.connect()

# -----------------------------
# 3. Find all raw parquet files
# -----------------------------
parquet_files = sorted(raw_dir.glob("yellow_tripdata_2024-*.parquet"))

print(f"Found {len(parquet_files)} parquet files.")

# -----------------------------
# 4. Clean each file and save it
# -----------------------------
for file_path in parquet_files:
    output_path = cleaned_dir / file_path.name

    print(f"Cleaning {file_path.name} -> {output_path.name}")

    query = f"""
    COPY (
        SELECT *
        FROM read_parquet('{file_path.as_posix()}')
        WHERE fare_amount >= 0
          AND trip_distance > 0
          AND tpep_dropoff_datetime >= tpep_pickup_datetime
          AND (tpep_dropoff_datetime - tpep_pickup_datetime) <= INTERVAL '6 hours'
    )
    TO '{output_path.as_posix()}'
    (FORMAT PARQUET);
    """

    con.execute(query)

print("Done. Cleaned files saved to data/cleaned/")