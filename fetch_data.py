import requests
import pandas as pd

# CoinGecko API endpoint for Bitcoin price
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,cardano,ripple"

r = requests.get(url)
data = r.json()

# Convert to DataFrame - THAT'S IT
df = pd.DataFrame(data)

# Look at it
print(df.head())

# Save to CSV
df.to_csv('crypto_prices.csv', index=False)

