import requests
import pandas as pd
from pathlib import Path

print(pd.Timestamp.now())
# CoinGecko API endpoint for Bitcoin price
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,cardano,ripple"

r = requests.get(url)
data = r.json()

# Convert to DataFrame - THAT'S IT
df = pd.DataFrame(data)

df['timestamp'] = pd.Timestamp.now()

# Look at it
print(df.head())

file_path = Path('crypto_prices.csv')
if file_path.exists():
    df.to_csv(file_path, header=False, mode='a',index=False)
else:
    df.to_csv(file_path, header=True, mode='w',index=False)


