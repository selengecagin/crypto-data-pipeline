import sys
import requests
import pandas as pd
import logging
from pathlib import Path

import sqlalchemy
from sqlalchemy import create_engine, text, VARCHAR
from sqlalchemy.exc import DBAPIError

logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,cardano,ripple"

try:
    r = requests.get(url, timeout=10, verify=True)
    r.raise_for_status()
    data = r.json()
    logging.info("API request completed successfully")
except requests.exceptions.HTTPError as errh:
    logging.error("HTTP error returned from API")
    sys.exit()
except requests.exceptions.ReadTimeout as errrt:
    logging.error("API request timed out")
    sys.exit()
except requests.exceptions.ConnectionError as conerr:
    logging.critical("Failed to establish connection to API")
    sys.exit()
except requests.exceptions.RequestException as errex:
    logging.error("Unexpected request exception occurred")
    sys.exit()

# Convert to DataFrame
df = pd.DataFrame(data)
df['timestamp'] = pd.Timestamp.now()
df['roi'] = df['roi'].astype(str)

engine = create_engine('postgresql+psycopg2://huriselengecagin:113308Monet@localhost/crypto_data_pipeline')

try:
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS crypto_prices (
            id VARCHAR,
            symbol VARCHAR,
            name TEXT,
            image TEXT,
            current_price NUMERIC,
            market_cap NUMERIC,
            market_cap_rank NUMERIC,
            fully_diluted_valuation NUMERIC,
            total_volume NUMERIC,
            high_24h NUMERIC,
            low_24h NUMERIC,
            price_change_24h NUMERIC,
            price_change_percentage_24h NUMERIC,
            market_cap_change_24h  NUMERIC,
            market_cap_change_percentage_24h NUMERIC,
            circulating_supply NUMERIC,
            total_supply NUMERIC,
            max_supply NUMERIC,
            ath NUMERIC,
            ath_change_percentage NUMERIC,
            ath_date TIMESTAMP,
            atl NUMERIC,
            atl_change_percentage NUMERIC,
            atl_date TIMESTAMP,
            roi TEXT,
            last_updated TIMESTAMP,
            timestamp TIMESTAMP
            )
        """))
except DBAPIError:
    logging.critical('Failed to create table in database.')
    sys.exit()

try:
    df.to_sql('crypto_prices', if_exists='append',index=False, con=engine)
    logging.info('Successfully appended records to crypto_prices table')
except DBAPIError:
    logging.critical('Failed to append dataframe to crypto_prices')
    sys.exit()

