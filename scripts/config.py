from pathlib import Path

# Automatically resolves the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define standard data directories
BRONZE_DIR = BASE_DIR / "data" / "bronze"
SILVER_DIR = BASE_DIR / "data" / "silver"
GOLD_DIR = BASE_DIR / "data" / "gold"

# Ensure directories exist
for folder in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
    folder.mkdir(parents=True, exist_ok=True)