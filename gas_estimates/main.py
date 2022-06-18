import os
import requests
import datetime

import pandas as pd

from web3 import Web3, HTTPProvider


ALCHEMY_API_KEY = os.environ['ALCHEMY_API_KEY']
web3 = Web3(HTTPProvider(f"https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}"))

api = "https://api.thegraph.com/subgraphs/name/convex-community/volume-mainnet-staging"

query = f'''
{{
  swapEvents (
    first: 1000,
    orderBy: timestamp,
    orderDirection: desc,
    where: {{pool: "{pool_addr.lower()}"}}
  ) {{
 	id
 	timestamp
 	block
    pool {{
      address
      name
    }}
    buyer
    tokenSold
    tokenBought
    amountSold
    amountSoldUSD
    amountBought
    amountBoughtUSD
    gasUsed
    gasLimit
  }}
}}
'''
r = requests.post(api, json={'query': query})
data = dict(r.json())["data"]["swapEvents"]

swaps_dict = []
for i in data:
    swaps_dict.append(
        {
            "tx_hash": i["id"].split('-')[0],
            "timestamp": datetime.datetime.fromtimestamp(int(i['timestamp'])),
            "block": int(i["block"]),
            "pool_addr": i["pool"]["address"],
            "pool_name": i["pool"]["name"],
            "buyer": i["buyer"],
            "token_sold": i["tokenSold"],
            "token_bought": i["tokenBought"],
            "amount_sold": float(i["amountSold"]),
            "amount_bought": float(i["amountBought"]),
            "amount_sold_usd": float(i["amountSoldUSD"]),
            "amount_bought_usd": float(i["amountBoughtUSD"]),
            "gas_used": float(i["gasUsed"]),
            "gas_limit": float(i["gasLimit"])
        }
    )
df_swaps = pd.DataFrame(swaps_dict)
df_swaps.set_index("timestamp", inplace=True)

def is_contract(addr: str) -> bool:
    return len(web3.eth.get_code(Web3.toChecksumAddress(addr))) > 0

df_swaps['buyer_is_contract'] = [is_contract(i) for i in df_swaps.buyer.values]


# some code to get single estimate: maybe average