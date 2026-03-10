from pathlib import Path
import duckdb

# -----------------------------
# 1. Set up folder paths
# -----------------------------
# Find the project root (one level above src)
# this makes the code more portable since it doesn't rely on hardcoded paths
# __file__ is the path to the current script, 
# resolve() gives the absolute path, 
# parent gives the directory, and we go up one level to get the project root
project_root = Path(__file__).resolve().parent.parent

raw_dir = project_root / "data" / "raw"
cleaned_dir = project_root / "data" / "cleaned"

# we create the cleaned directory if it doesn't exist,
# parents=True allows it to create any missing parent directories as well,
# exist_ok=True means it won't raise an error if the directory already exists
# now later we can save cleaned files to cleaned_dir 
# without worrying about whether the folder exists or not
cleaned_dir.mkdir(parents=True, exist_ok=True)

# -----------------------------
# 2. Connect to DuckDB
# -----------------------------
# connect() creates a new DuckDB connection object that we can use to run SQL queries
# which we do at the end of step 4 to clean the data
con = duckdb.connect()

# -----------------------------
# 3. Find all raw parquet files
# -----------------------------
# glob() searches the directory for matching files
# we sort them to ensure consistent processing order
# now parquet_files is a list of Path objects pointing to each raw parquet file
parquet_files = sorted(raw_dir.glob("yellow_tripdata_2024-*.parquet"))

# the f string allows us to easily include the number of files found in the print statement
# because everything inside {} is replaced with the value of the expression,
# and inserted into the string at that position
print(f"Found {len(parquet_files)} parquet files.")

# -----------------------------
# 4. Clean each file and save it
# -----------------------------
# The cleaning criteria are:
# - fare_amount >= 0
# - trip_distance > 0
# - dropoff time is after pickup time
# - trip duration is less than 6 hours (to filter out outliers)
# even though duckdb can read all files together,
# these queries will be more efficient if we process one file at a time 
# and save the cleaned version
# the reason we need file_path.as_posix() is that duckdb expects file paths as strings, 
# and as_posix() converts the Path object to a string with forward slashes, 
# which works on all platforms
for file_path in parquet_files:
    output_path = cleaned_dir / file_path.name

    print(f"Cleaning {file_path.name} -> {output_path.name}")

    # f""" allows us to write a multi-line SQL query as a string,
    # and we can still use {file_path.as_posix()} to insert the file path into the query
    # i.e. f""" means multiline string with variable interpolation
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