import sys
from xml.dom.expatbuilder import TEXT_NODE
import requests
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text, VARCHAR
from sqlalchemy.dialects.mysql import NUMERIC

# CoinGecko API endpoint for Bitcoin price
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,cardano,ripple"

try:
    r = requests.get(url, timeout=10,verify=True)
    r.raise_for_status()
    data = r.json()
except requests.exceptions.HTTPError as errh:
    print("HTTP Error")
    print(errh.args[0])
    sys.exit()
except requests.exceptions.ReadTimeout as errrt:
    print("Time out")
    sys.exit()
except requests.exceptions.ConnectionError as conerr:
    print("Connection error")
    sys.exit()
except requests.exceptions.RequestException as errex:
    print("Exception request")
    sys.exit()


# Convert to DataFrame
df = pd.DataFrame(data)
df['timestamp'] = pd.Timestamp.now()

engine = create_engine('postgresql+psycopg2://huriselengecagin:113308Monet@localhost/crypto_data_pipeline')

# Create table if it doesn't exist
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
df['roi'] = df['roi'].astype(str)

df.to_sql('crypto_prices', if_exists='append',index=False, con=engine)

# file_path = Path('crypto_prices.csv')
# if file_path.exists():
#     df.to_csv(file_path, header=False, mode='a',index=False)
# else:
#     df.to_csv(file_path, header=True, mode='w',index=False)


