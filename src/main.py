from supported_chains import chains
from prices import get_usd_price
from pprint import pprint
import requests
import click

# TODO: TXS and Tokens to dataclasses

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
				'token_name': chain['token_name'],
				'token_symbol': chain['token_symbol'],
				'gas_cost': usd_price * int(tx['gas'])*int(tx['gasPrice'])/10**18
			})

	return normal_txs


def get_erc20_transactions(chain, account):
	erc20_tx_request = (
		"?module=account"
		"&action=tokentx"
		f"&address={account}"
		"&startblock=0"
		"&endblock=99999999"
	)
	r = requests.get(f"{chain['etherscan_url']}{erc20_tx_request}&apikey={chain['etherscan_api_key']}")
	chain_txs = r.json()['result']
	erc20_txs = []

	for tx in chain_txs:
		ts = tx['timeStamp']
		direction = 1 if tx['to'].lower() == account.lower() else -1
		token_decimal = int(tx['tokenDecimal'])
		token_value = direction * int(tx['value'])/10**token_decimal
		token_symbol = tx['tokenSymbol']
		token_name = tx['tokenName']
		usd_price = get_usd_price(token_symbol, ts)
		usd_value = token_value * usd_price if usd_price else None
		erc20_txs.append({
			'chain_name': chain['name'],
			'timestamp': ts,
			'from': tx['from'],
			'to': tx['to'],
			'value': token_value,
			'usd_price': usd_price,
			'usd_value': usd_value,
			'token_name': token_name,
			'token_symbol': token_symbol,
			'gas_used': int(tx['gas'])*int(tx['gasPrice'])/10**18
		})

	return erc20_txs


def get_all_transactions(account):
	all_txs = []

	for chain in chains:
		# normal_txs = get_normal_transactions(chain, account)
		# all_txs.extend(normal_txs)

		erc20_txs = get_erc20_transactions(chain, account)
		all_txs.extend(erc20_txs)

	pprint(all_txs)
	print(len(all_txs))


if __name__ == "__main__":
	get_all_transactions("0x4e83362442b8d1bec281594cea3050c8eb01311c")
	