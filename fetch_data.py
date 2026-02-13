import requests

# CoinGecko API endpoint for Bitcoin price
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

r = requests.get(url)

# Print the status code
print(r.status_code)

# Print the result
print(r.json())

