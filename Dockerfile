FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install basic system build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt-get/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers & required Linux system dependencies
RUN playwright install --with-deps chromium

# Copy rest of the project
COPY . .

CMD ["bash", "-c", "python scripts/1bhk_scrapper.py && python scripts/2bhk_scrapper.py && python scripts/3bhk_scrapper.py && python scripts/silver_transform.py && python scripts/gold_transform.py"]