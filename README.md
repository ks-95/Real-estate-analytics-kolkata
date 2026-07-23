# 🏢 Real Estate Data Pipeline (Medallion Architecture)

An end-to-end automated data pipeline that scrapes, cleans, transforms, and loads Kolkata real estate listing data into a PostgreSQL database using Docker and Python.

---

## 🏗️ Architecture Overview

The pipeline follows the **Medallion Architecture** (Bronze ➔ Silver ➔ Gold) to process scraped property listings across multiple categories (1 BHK, 2 BHK, 3 BHK):



### Data Pipeline Stages
* **Bronze Layer:** Ingests raw JSON output directly from web scrapers across 1 BHK, 2 BHK, and 3 BHK directories.
* **Silver Layer:** Validates schema, handles missing/malformed attributes, cleans raw text, and standardizes geographic regions into sectors (e.g., South Kolkata, Howrah).
* **Gold Layer:** Consolidates multi-file listings into a single aggregated dataset (450+ records) optimized for analytical querying.
* **Database Storage:** Persists the finalized Gold layer dataset into a PostgreSQL instance for downstream analytics and dashboards.

---

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **Data Processing:** Pandas, Pathlib
* **Database:** PostgreSQL
* **Containerization:** Docker, Docker Compose

---

## 📁 Repository Structure

.
├── scripts/
│   ├── scraper.py          # Data extraction scripts
│   ├── silver_transform.py # Data cleaning and transformation pipeline
│   └── gold_load.py        # Database loader script
├── data/
│   ├── bronze/             # Raw scraped JSON files (1BHK, 2BHK, 3BHK)
│   ├── silver/             # Cleaned intermediate files
│   └── gold/               # Analytics-ready data
├── docker-compose.yml      # Multi-container orchestration
├── Dockerfile              # Python environment definition
├── requirements.txt        # Python dependencies
└── README.md

## 🚀 Getting Started

### Prerequisites

* Docker Desktop installed and running.
* Git installed on your local machine.

### Installation & Execution

1. Clone the repository:
   git clone https://github.com/ks-95/Real-estate-analytics-kolkata.git
   cd Real-estate-analytics-kolkata

2. Configure Environment Variables:
   Create a .env file in the root directory:
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=real_estate_db
   POSTGRES_HOST=real_estate_postgres
   POSTGRES_PORT=5432

3. Build and Run with Docker Compose:
   docker-compose up --build

Once complete, the pipeline will process all bronze files, clean and aggregate them, write to PostgreSQL ("Data saved to Postgres db"), and exit cleanly (code 0).
