import sys
import json
from pathlib import Path
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from clean_string import clean_string
from dotenv import load_dotenv
import os


# Ensure console output uses UTF-8 on Windows so the rupee symbol prints correctly.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass
load_dotenv()
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "new_password")
db_host = os.getenv("DB_HOST", "localhost")  # Overridden to 'postgres_db' inside Docker
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "real_estate_db")

engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)
records = []
bronze_paths = {
    "1BHK": Path("/app/data/bronze/one_bhk_data"),
    "2BHK": Path("/app/data/bronze/two_bhk_data"),
    "3BHK": Path("/app/data/bronze/three_bhk_data"),
}
silver_path = Path("/app/data/silver")
silver_path.mkdir(parents=True, exist_ok=True)

latest_files = {}

for key, path in bronze_paths.items():
    json_files = list(path.glob("*.json"))
    
    if not json_files:
        raise FileNotFoundError(
            f"No JSON files found in {key} directory: {path}. "
            f"Ensure the scrapers executed and generated data before running silver_transform."
        )
    
    # default parameter prevents ValueError if sequence is empty, though checked above
    latest_files[key] = max(json_files, key=lambda f: f.stat().st_mtime)

# Unpack for direct use if needed:
latest_file_1bhk = latest_files["1BHK"]
latest_file_2bhk = latest_files["2BHK"]
latest_file_3bhk = latest_files["3BHK"]


with open(latest_file_1bhk, "r", encoding="utf-8") as f:
    raw_1bhk_data = json.load(f)

for value in raw_1bhk_data:
    records.append({
        "title" : value.get("title"),
        "price" : clean_string(value.get("price")),
        "price_per_sqft" : clean_string(value.get("price_per_sqft")),
        "carepet_area" : clean_string(value.get("carpet_area"))
    })
with open(latest_file_2bhk, "r", encoding="utf-8") as f:
    raw_2bhk_data = json.load(f)
for value in raw_2bhk_data:
    records.append({
        "title" : value.get("title"),
        "price" : clean_string(value.get("price")),
        "price_per_sqft" : clean_string(value.get("price_per_sqft")),
        "carepet_area" : clean_string(value.get("carpet_area"))
    })
with open(latest_file_3bhk, "r", encoding="utf-8") as f:
    raw_3bhk_data = json.load(f)
for value in raw_3bhk_data:
    records.append({
        "title" : value.get("title"),
        "price" : clean_string(value.get("price")),
        "price_per_sqft" : clean_string(value.get("price_per_sqft")),
        "carepet_area" : clean_string(value.get("carpet_area"))
    })


print(records)

df = pd.DataFrame(records)

print(df)
#df['price'] = df['price'].replace('', np.nan)
df['price_per_sqft'] = df['price_per_sqft'].replace('', np.nan)

parquet_file = silver_path / "real_estate_cleaned.parquet"
df.to_parquet(parquet_file, index=False)

print(f"Parquet saved at: {parquet_file}")

# Load into PostgreSQL
df.to_sql(
    "real_estate_cleaned_data",
    engine,
    if_exists="append",
    index=False
)

print("Data loaded into PostgreSQL successfully!")