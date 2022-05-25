import itertools
import typing
from core.coins import (
    ETH,
    ETH_WETH_POOL,
    WETH,
    WETH_ETH_POOL,
)
from core.common import BasePool, Coin, Swap
from src.utils.constants import SUBGRAPH_API
from src.core.path_finders.depth_first import DepthFirstSearch
from utils.subgraph import get_pool_data, get_latest_pool_coin_reserves

RESERVE_THRESHOLD = 100  # num coins of each type in the pool


def compile_graph(
    network_name: str, base_pools: typing.List[BasePool]
) -> DepthFirstSearch:

    # query subgraph for pools in network_name
    data = get_pool_data(SUBGRAPH_API[network_name])
    base_pool_tokens = [base_pool.lp_token for base_pool in base_pools]

    # select pools with coins greater than RESERVE_THRESHOLD:
    vetted_pools = []
    for pool_data in data:

        pool_address = pool_data["address"]
        coin_decimals = [int(i) for i in pool_data["coinDecimals"]]
        latest_coin_reserves = get_latest_pool_coin_reserves(
            pool_addr=pool_address, api=SUBGRAPH_API[network_name]
        )
        pool_reserve_critera_met = all(
            [
                reserves > RESERVE_THRESHOLD * 10 ** coin_decimals[idx]
                for idx, reserves in enumerate(latest_coin_reserves)
            ]
        )

        if not pool_reserve_critera_met:
            continue

        vetted_pools.append(pool_data)

    # get coins in vetted pools:
    all_coins_in_vetted_pools = []
    for pool in vetted_pools:
        for idx, coin in enumerate(pool["coins"]):
            all_coins_in_vetted_pools.append(coin)

    all_coins_in_vetted_pools = list(set(all_coins_in_vetted_pools))

    # init coin map:
    path_finder = DepthFirstSearch(all_coins_in_vetted_pools)

    # add weth <-> eth wrapper contract:
    path_finder.coin_map.add_pair(WETH, ETH, WETH_ETH_POOL)
    path_finder.coin_map.add_pair(ETH, WETH, ETH_WETH_POOL)

    # add the rest of the pairs:
    for pool in vetted_pools:

        pool_address = pool["address"]
        is_cryptoswap = pool["isV2"] == "true"
        is_metapool = pool["metapool"] == "true"

        # get all coins in the pool:
        coins_in_pool = []
        for idx, coin in enumerate(pool["coins"]):
            coin_dataclass = Coin(
                address=coin,
                network=network_name,
                decimals=int(pool["coinDecimals"][idx]),
                is_lp_token=coin in base_pool_tokens
            )
            coins_in_pool.append(coin_dataclass)

        # if is_metapool, then find underlying coins and add them:
        base_pool = None
        if is_metapool:
            for base_pool in base_pools:
                if base_pool.lp_token in coins_in_pool:
                    coins_in_pool.extend(base_pool.coins)
                    break  # stores base pool dataclass in base_pool

        # update coin_map in path_finder:
        coin_permutations = list(itertools.permutations(coins_in_pool))
        for coin_permutation in coin_permutations:

            coin_a: Coin = coin_permutation[0]
            coin_b: Coin = coin_permutation[1]

            # get indices of coin_a and coin_b:
            i = pool["coins"].index(coin_a.address)
            j = pool["coins"].index(coin_b.address)

            # it is an underlying swap if either coin is a base_pool lp_token
            is_underlying_swap = (
                is_metapool and (coin_a.is_lp_token or coin_b.is_lp_token)
            )

            # make swap object:
            swap = Swap(
                pool=pool_address,
                network=network_name,
                i=i,
                j=j,
                coin_a=coin_a.address,
                coin_a_decimals=coin_a.decimals,
                coin_b=coin_b.address,
                coin_b_decimals=coin_b.decimals,
                is_cryptoswap=is_cryptoswap,
                is_stableswap=not is_cryptoswap,
                is_metapool=is_metapool,
                is_underlying_swap=is_underlying_swap,
                base_pool=pool["basePool"]
            )

            path_finder.coin_map.add_pair(
                coin_a, coin_b, swap
            )

    return path_finder
