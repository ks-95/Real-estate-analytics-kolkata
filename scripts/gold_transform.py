import sys
import numpy as np
import json
import re
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from clean_string import clean_string
from dotenv import load_dotenv
import os

load_dotenv()
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "new_password")
db_host = os.getenv("DB_HOST", "localhost")  # Overridden to 'postgres_db' inside Docker
db_port = os.getenv("DB_PORT", "5432")
db_name = os.getenv("DB_NAME", "real_estate_db")

engine = create_engine(
    f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
)

#silver_path = Path(r"C:\Users\KANAK\scraping\data\silver")
gold_path = Path(r"C:\Users\KANAK\scraping\data\gold")
gold_path.mkdir(parents=True, exist_ok=True)

query = "SELECT * FROM real_estate_cleaned_data"

df = pd.read_sql(query, engine)
df["price"] = pd.to_numeric(df["price"], errors="coerce").astype("Int64")
df["price_per_sqft"] = pd.to_numeric(df["price_per_sqft"], errors="coerce").astype("float64")

print("Silver Data:")
print(df)

def extract_area(text):
  
      # 1. Strip 'Kolkata' and trailing spaces/commas from the right
    cleaned = re.sub(r',\s*kolkata.*$', '', text, flags=re.IGNORECASE).strip()
    
    # 2. Extract text after 'Sale in' or 'for Sale in'
    match = re.search(r'for\s+Sale\s+in\s+(.*)', cleaned, flags=re.IGNORECASE)
    if match:
        location_part = match.group(1).strip()
        
        # Split by comma to inspect address parts
        parts = [p.strip() for p in location_part.split(',')]
        
        # If there are multiple parts (e.g., ["Nidhi The 105 2", "Bangur", "Lake Town"])
        # The landmark/locality is usually the 2nd part or 1st part depending on building name
        if len(parts) >= 3:
            return parts[1]  # Captures 'Bangur'
        elif len(parts) >=2:
            return parts[1]  # Captures 'Behala Chowrasta'
        else:
            return parts[0]
            
    return cleaned



sectors = ['IT Sector', 'North Kolkata', 'South Kolkata', 'Central Kolkata', 'Howrah']


df['bhk'] = df['title'].str.extract(r'(\d+)\s*BHK', flags=re.IGNORECASE, expand=False)
#df['area'] = df['title'].str.extract(r',\s*([^,]+)\s*,\s*kolkata', flags=re.IGNORECASE, expand=False).fillna('')

#df['area'] = df['area'].str.strip()
df['area'] = df['title'].apply(extract_area)
conditions = [
    # 1. IT / Tech Sector
    df['area'].str.lower().str.contains(
        'salt lake|new town|rajarhat|sector 5|sector v|action area|chinar park', 
        na=False
    ),
    
    # 2. North Kolkata
    df['area'].str.lower().str.contains(
        'dum dum|shyambazar|lake town|vip road|kankurgachi|barasat|baguiati|kestopur|sodepur|barrackpore|birati|baranagar|paikpara|kaikhali|tegharia|rathtala', 
        na=False
    ),
    
    # 3. South Kolkata
    df['area'].str.lower().str.contains(
        'joka|garia|tollygunge|ballygunge|behala|jadavpur|kasba|ajoy nagar|santoshpur|baghajatin|bansdroni|chetla|dhakuria|selimpur|ekdalia|fartabad|new garia|naktala|baishnabghata|haridevpur|paschim putiary|sonarpur|narendrapur|kamalgazi|patuli|netaji nagar|new alipore|mukundapur|nayabad|purba barisha|sakher bazar|topsia', 
        na=False
    ),
    
    # 4. Central Kolkata
    df['area'].str.lower().str.contains(
        'park street|camac street|dalhousie|entally|sealdah|bowbazar|middleton|sn banerjee|triangular park', 
        na=False
    ),
    
    # 5. Howrah & Suburbs (Optional 5th Sector)
    df['area'].str.lower().str.contains(
        'howrah|salkia|serampore|uttarpara|konnagar|dankuni|bhangar|chunavati|fuleswar|kadamtala|bantra', 
        na=False
    )
]
df['sector'] = np.select(conditions, sectors, default='Other')
print("gold df")

print(df)

parquet_file = gold_path / "real_estate_aggregated.parquet"
df.to_parquet(parquet_file, index=False)

df_cleaned = df.dropna(subset=['title', 'price','price_per_sqft'])
df_cleaned = df_cleaned.drop_duplicates()

df_cleaned.to_sql(
    "real_estate_aggregated_data",
    engine,
    if_exists="replace",
    index=False
)

print("Data saved to Postgres db")
