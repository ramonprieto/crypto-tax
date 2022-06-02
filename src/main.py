from supported_chains import chains
from prices import get_usd_price
from pprint import pprint
import requests
import click


def get_normal_transactions(chain, account):
	normal_tx_request = (
		"?module=account"
		"&action=txlist"
		f"&address={account}"
		"&startblock=0"
		"&endblock=99999999"
	)
	r = requests.get(f"{chain['etherscan_url']}{normal_tx_request}&apikey={chain['etherscan_api_key']}")
	chain_txs = r.json()['result']
	normal_txs = []

	for tx in chain_txs:
		if tx['isError'] == '0':
			ts = tx['timeStamp']
			direction = 1 if tx['to'].lower() == account.lower() else -1
			native_value = direction * int(tx['value'])/10**18
			usd_price = get_usd_price("ETH", ts)
			usd_value = native_value * usd_price
			normal_txs.append({
				'chain_name': chain['name'],
				'timestamp': ts,
				'from': tx['from'],
				'to': tx['to'],
				'value': native_value,
				'usd_price': usd_price,
				'usd_value': usd_value,
				'token': chain['token'],
				'gas_cost': usd_price * int(tx['gas'])*int(tx['gasPrice'])/10**18
			})

	return normal_txs


def get_all_transactions(account):
	all_txs = []

	for chain in chains:
		normal_txs = get_normal_transactions(chain, account)
		all_txs.extend(normal_txs)

	pprint(all_txs)
	print(len(all_txs))


if __name__ == "__main__":
	get_all_transactions("0x541D67bEdBfe820b4E58712bf032C7250548D733")
	