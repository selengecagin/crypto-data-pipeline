# Crypto Data Pipeline

## Overview
A Python ETL pipeline that fetches cryptocurrency prices from CoinGecko API and stores them in PostgreSQL. Runs every minute to build historical price data.

## How It Works
Fetches live prices for 5 cryptocurrencies
Stores data in PostgreSQL with timestamps
Handles API failures gracefully
Logs all operations
Runs automatically on a schedule

## High Level Architecture

                   ┌────────────────────────┐
                   │     CoinGecko API      │
                   │   /coins/markets       │
                   └────────────┬───────────┘
                                │
                                │ HTTPS Request
                                ▼
                 ┌────────────────────────────┐
                 │        Ingestion Layer     │
                 │  requests + error control  │
                 └────────────┬───────────────┘
                              │ JSON payload
                              ▼
                 ┌────────────────────────────┐
                 │    Transformation Layer    │
                 │     pandas DataFrame       │
                 └────────────┬───────────────┘
                              │ Structured rows
                              ▼
                 ┌────────────────────────────┐
                 │        Persistence Layer   │
                 │    SQLAlchemy → Postgres   │
                 └────────────┬───────────────┘
                              │
                              ▼
                 ┌────────────────────────────┐
                 │      crypto_prices Table   │
                 │        PostgreSQL          │
                 └────────────────────────────┘

## Technology Stack

| Layer           | Technology    | Role                   |
| --------------- | ------------- | ---------------------- |
| Language        | Python        | Core runtime           |
| HTTP            | requests      | API communication      |
| Data Processing | pandas        | Transformation         |
| ORM / DB Layer  | SQLAlchemy    | DB abstraction         |
| Database        | PostgreSQL    | Persistent storage     |
| Scheduling      | schedule      | Job orchestration      |
| Config          | python-dotenv | Environment management |
| Logging         | logging       | Observability          |


## Dependencies and Installation
----------------------------
To install the crypto data pipeline, please follow these steps:

1. Clone the repository to your local machine.
   ```
   git clone https://github.com/selengecagin/crypto-data-pipeline
   cd crypto-data-pipeline
   ```
2. Create virtual environment
   ```
   python -m venv venv
   source venv/bin/activate
   ```
3. Install the required dependencies by running the following command:
   ```
   pip install -r requirements.txt
   ```
4. Set up PostgreSQL database
   ``` 
   psql -U postgres
   CREATE DATABASE crypto_data_pipeline;
   \q
   ```
5. Create .env file in project root
   ```
    echo "db_password=your_postgres_password" > .env
   ```   
8. Run the pipeline
   ```
   python fetch_data.py
   ```

## What I Learned 🚀
- Building ETL pipelines
- Error handling in production systems
- Database schema design
- Logging and monitoring
