import requests

API_KEY = "f4613894a30509f48eaebf914f661335b28857367e950ea60a2e25c0300661e1"


def get_usd_price(symbol, ts):
	price_feed_url = (
		"https://min-api.cryptocompare.com"
		"/data/pricehistorical"
		f"?fsym={symbol}&tsyms=USD&ts={ts}&api_key={API_KEY}"
	)
	r = requests.get(price_feed_url)
	results = r.json()

	try:
		usd_price = results[symbol]['USD']
	except KeyError:
		usd_price = None

	return usd_price