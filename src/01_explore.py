# import necessary libraries
import duckdb
import pandas as pd
from pathlib import Path

# define project paths
project_root = Path("/Users/saraneff/Desktop/data-project")

cleaned_dir = project_root / "data" / "cleaned"
raw_dir = project_root / "data" / "raw"

# connect to duckdb
con = duckdb.connect()

# load all 12 cleaned parquet files into a single dataframe
trips = con.execute(f"""
    SELECT *
    FROM read_parquet('{cleaned_dir.as_posix()}/yellow_tripdata_2024-*.parquet')
    LIMIT 5
""").fetchdf()

print(trips.head())