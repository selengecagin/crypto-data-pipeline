import requests

# CoinGecko API endpoint for Bitcoin price
url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana,cardano,ripple"

r = requests.get(url)

# Print the status code
print(r.status_code)

# Print the result
print(r.json())

