import itertools
import typing

from router.coins import ETH, ETH_WETH_POOL, WETH, WETH_ETH_POOL
from router.common import BasePool, Coin, Swap
from router.core import Router
from router.utils.constants import SUBGRAPH_API
from utils.subgraph import get_latest_pool_coin_reserves, get_pool_data


RESERVE_THRESHOLD = 100  # num coins of each type in the pool


def init_router(
    network_name: str, base_pools: typing.List[BasePool]
) -> Router:

    # query subgraph for pools in network_name
    data = get_pool_data(SUBGRAPH_API[network_name])
    base_pool_tokens = [base_pool.lp_token.address for base_pool in base_pools]

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
    router = Router(all_coins_in_vetted_pools)

    # add weth <-> eth wrapper contract:
    router.coin_map.add_pair(WETH, ETH, WETH_ETH_POOL)
    router.coin_map.add_pair(ETH, WETH, ETH_WETH_POOL)

    # add the rest of the pairs:
    for pool in vetted_pools:

        pool_address = pool["address"]
        is_cryptoswap = pool["isV2"]
        is_metapool = pool["metapool"]

        # get all coins in the pool:
        coins_in_pool = []
        for idx, coin in enumerate(pool["coins"]):
            coin_dataclass = Coin(
                address=coin,
                network=network_name,
                decimals=int(pool["coinDecimals"][idx]),
                is_lp_token=coin in base_pool_tokens,
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
            swap_involves_lp_token = coin_a.is_lp_token or coin_b.is_lp_token

            # we extended coins_in_pool to include base_pool's lp_token and the
            # individual coins in the base_pool on top of the metapool paired
            # coin. Ignore all pairs between base_pool and its underlying
            # because that's add/remove liquidity and not exchange:
            if (
                    is_metapool and
                    swap_involves_lp_token and
                    len(
                        {coin_a, coin_b}.intersection(
                            set(base_pool.coins)
                        )
                    ) > 0
            ):
                continue

            # it is an underlying swap if it is a metapool and lp token
            # isn't being swapped:
            is_underlying_swap = is_metapool and not (
                coin_a.is_lp_token or coin_b.is_lp_token
            )

            # get indices of coin_a and coin_b:
            if not is_underlying_swap:
                i = pool["coins"].index(coin_a.address)
                j = pool["coins"].index(coin_b.address)
            else:
                i = 0
                j = 0
                if coin_a in base_pool.coins:
                    i_base = base_pool.coins.index(coin_a)
                    i = i_base + 1
                if coin_b in base_pool.coins:
                    j_base = base_pool.coins.index(coin_b)
                    j = j_base + 1

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
                base_pool=pool["basePool"],
            )

            router.coin_map.add_pair(coin_a, coin_b, swap)

    return router
