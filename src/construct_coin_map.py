import itertools
import typing
from core.coins import (
    ETH,
    ETH_WETH_POOL,
    THREECRV_BASEPOOL,
    WETH,
    WETH_ETH_POOL,
)
from core.common import BasePool, CoinMap, Coin, PathFinder, Pool
from core.constants import SUBGRAPH_API
from core.path_finders.depth_first import DepthFirstSearch
from utils.subgraph import get_pool_data, get_latest_pool_coin_reserves

RESERVE_THRESHOLD = 100  # num coins of each type in the pool


def compile_graph(
    network_name: str, base_pools: typing.List[BasePool]
) -> typing.Any[DepthFirstSearch, PathFinder]:

    # query subgraph for pools in network_name
    data = get_pool_data(SUBGRAPH_API[network_name])

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
    path_finder = DepthFirstSearch(
        all_coins_in_vetted_pools, base_pools=[THREECRV_BASEPOOL]
    )

    # add weth <-> eth as the first pair:
    path_finder.coin_map.add_pair(WETH, ETH, WETH_ETH_POOL)
    path_finder.coin_map.add_pair(ETH, WETH, ETH_WETH_POOL)

    # add the rest of the pairs:
    for pool in vetted_pools:
        pool_address = pool["address"]
        coins_in_pool = []
        for idx, coin in enumerate(pool["coins"]):
            coin_dataclass = Coin(
                address=coin,
                network=network_name,
                decimals=int(pool["coinDecimals"][idx]),
            )
            coins_in_pool.append(coin_dataclass)

        # if the pair contains BasePool lp token, make pairs with underlying
        # coins as well:
        for base_pool in base_pools:
            if base_pool.lp_token in coins_in_pool:
                coins_in_pool.extend(base_pool.coins)

        # update coin_map in path_finder:
        coin_permutations = list(itertools.permutations(coins_in_pool))
        for coin_permutation in coin_permutations:
            coin_pair_pool = Pool(
                address=pool_address,
                network=network_name,
                coin_a=coin_permutation[0],
                coin_b=coin_permutation[1],
            )

            path_finder.coin_map.add_pair(
                coin_permutation[0], coin_permutation[1], coin_pair_pool
            )

    return path_finder
