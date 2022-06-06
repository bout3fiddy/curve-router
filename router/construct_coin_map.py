import itertools
import time
import typing

from brownie import ZERO_ADDRESS

from router.common import BasePool, Swap
from router.constants import ETH, SUBGRAPH_API, TRICRYPTO2, WETH
from router.core import Router
from router.misc import Timer
from router.subgraph import get_pool_data

RESERVE_THRESHOLD = 100  # num coins of each type in the pool


def init_router(
    network_name: str, base_pools: typing.List[BasePool]
) -> Router:

    # query subgraph for pools in network_name
    with Timer() as t:
        data = get_pool_data(SUBGRAPH_API[network_name])
    print(f"Downloaded data from the graph. Took {t.interval:.04f} seconds.")

    base_pool_lp_tokens = [base_pool.lp_token for base_pool in base_pools]

    # select pools with coins greater than RESERVE_THRESHOLD:
    print("Removing illiquid pools ...")
    with Timer() as t:
        vetted_pools = []
        for pool_data in data:

            coin_decimals = [int(i) for i in pool_data["coinDecimals"]]
            latest_coin_reserves = pool_data["reserves"]
            pool_reserve_critera_met = all(
                [
                    reserves > RESERVE_THRESHOLD * 10 ** coin_decimals[idx]
                    for idx, reserves in enumerate(latest_coin_reserves)
                ]
            )

            if not pool_reserve_critera_met:
                continue

            vetted_pools.append(pool_data)

    print(
        f"Number of pools shortlisted: {len(vetted_pools)}. "
        f"Took {t.interval:.04f} seconds."
    )

    # get coins in vetted pools:
    all_coins_in_vetted_pools = []
    for pool in vetted_pools:
        for idx, coin in enumerate(pool["coins"]):
            all_coins_in_vetted_pools.append(coin)

    all_coins_in_vetted_pools = list(set(all_coins_in_vetted_pools))

    # init coin map:
    router = Router(all_coins_in_vetted_pools)

    # add basepool add and remove liquidity options, but ignore this path later
    for base_pool in base_pools:
        lp_token = base_pool.lp_token
        base_pool_addr = base_pool.pool_address
        base_pool_reserves_usd = 0
        for i in vetted_pools:
            if i["address"] == base_pool_addr:
                base_pool_reserves_usd = i["reservesUsd"]
                break

        # if lending pool, add and removes are always underlying=True. This is
        # because Swaps.vy only considers add and remove liquidity with
        # `use_underlying: bool = True` in `exchange_multiple`: line 562 and
        # 568.
        base_pool_coins = base_pool.coins
        is_underlying = False
        if base_pool.underlying_coins:
            is_underlying = True
            base_pool_coins = base_pool.underlying_coins

        # add liquidity:
        for i, coin in enumerate(base_pool.coins):

            swap = Swap(
                pool=base_pool_addr,
                network=network_name,
                i=i,
                j=9,  # Swaps.vy, L554. Param takes `i` not `j`
                coin_a=coin,
                coin_b=lp_token,
                is_cryptoswap=base_pool.is_cryptoswap,
                is_stableswap=not base_pool.is_cryptoswap,
                is_metapool=False,
                is_underlying=is_underlying,
                is_add_liquidity=True,
                base_pool=ZERO_ADDRESS,
                pool_tvl_usd=sum(base_pool_reserves_usd),
                num_coins_pool=len(base_pool_reserves_usd)
            )
            router.coin_map.add_pair(coin, lp_token, swap)

        # remove liquidity:
        for j, coin in enumerate(base_pool_coins):

            swap = Swap(
                pool=base_pool_addr,
                network=network_name,
                i=9,  # it is not a swap so input coin for add liquidity is 9
                j=j,  # Swaps.vy, L568. Param takes `j` not `i`
                coin_a=lp_token,
                coin_b=coin,
                is_cryptoswap=base_pool.is_cryptoswap,
                is_stableswap=not base_pool.is_cryptoswap,
                is_metapool=False,
                is_underlying=is_underlying,
                is_remove_liquidity=True,
                base_pool=ZERO_ADDRESS,
                pool_tvl_usd=sum(base_pool_reserves_usd),
                num_coins_pool=len(base_pool_reserves_usd)
            )
            router.coin_map.add_pair(lp_token, coin, swap)

    # add the rest of the pairs:
    print("Adding coins into path finder's coin map...")
    tic = time.perf_counter()
    num_pairs = 0
    for pool in vetted_pools:

        pool_address = pool["address"]
        is_cryptoswap = pool["isV2"]

        # for tricrypto2 use weth for swaps. for other crypto pools, use eth.
        # this is due to gas reasons mentioned by mich.
        use_eth = True
        if (
                is_cryptoswap and
                pool_address == TRICRYPTO2 and
                network_name == "Mainnet"
        ):
            use_eth = False
        is_metapool = pool["metapool"]
        coins_in_pool = pool["coins"]
        pool_reserves_usd = pool["reservesUsd"]

        # If is_metapool, then find underlying coins and add them. If lending
        # pool, then use `underlying_coins` to avoid aTokens
        base_pool = None
        if is_metapool:
            for base_pool in base_pools:
                base_pool_coins = base_pool.coins
                if base_pool.is_lending:
                    base_pool_coins = base_pool.underlying_coins
                if base_pool.lp_token in coins_in_pool:
                    coins_in_pool.extend(base_pool_coins)
                    break  # stores base pool dataclass in base_pool

        # update coin_map in path_finder:
        coin_pairs = list(itertools.combinations(coins_in_pool, 2))
        for coin_pair in coin_pairs:

            coin_a = coin_pair[0]
            coin_b = coin_pair[1]

            # we extended coins_in_pool to include base_pool's lp_token and the
            # individual coins in the base_pool on top of the metapool paired
            # coin. Ignore all pairs between base_pool and its underlying
            # because that's add/remove liquidity and not exchange:
            swap_involves_basepool_lp_token = (
                coin_a in base_pool_lp_tokens or coin_b in base_pool_lp_tokens
            )
            swap_involves_basepool_underlying_token = (
                is_metapool
                and len({coin_a, coin_b}.intersection(set(base_pool.coins)))
                > 0
            )
            if (
                swap_involves_basepool_lp_token
                and swap_involves_basepool_underlying_token
            ):
                continue

            # if the pool is a metapool and both coins are in the base pool,
            # then remove them (since the basepool is sufficient for those
            # swaps):
            if (
                is_metapool
                and coin_a in base_pool.coins
                and coin_b in base_pool.coins
            ):
                continue

            # it is an underlying swap if it is a metapool and lp token
            # isn't being swapped:
            is_underlying = (
                is_metapool and not swap_involves_basepool_lp_token
            )

            # get indices of coin_a and coin_b:
            if not is_underlying:
                i = pool["coins"].index(coin_a)
                j = pool["coins"].index(coin_b)
            else:  # underlying swap indices are different:
                i = 0
                j = 0
                if coin_a in base_pool.coins:
                    i_base = base_pool.coins.index(coin_a)
                    i = i_base + 1
                if coin_b in base_pool.coins:
                    j_base = base_pool.coins.index(coin_b)
                    j = j_base + 1

            zap_address = ZERO_ADDRESS
            if is_metapool and base_pool.is_lending:
                zap_address = base_pool.zap_address

            # make swap object:
            swap = Swap(
                pool=pool_address,
                zap_address=zap_address,
                network=network_name,
                i=i,
                j=j,
                coin_a=coin_a,
                coin_b=coin_b,
                is_cryptoswap=is_cryptoswap,
                use_eth=use_eth,
                is_stableswap=not is_cryptoswap,
                is_metapool=is_metapool,
                is_underlying=is_underlying,
                base_pool=pool["basePool"],
                pool_tvl_usd=sum(pool_reserves_usd),
                num_coins_pool=len(pool_reserves_usd)
            )
            router.coin_map.add_pair(coin_a, coin_b, swap)
            num_pairs += 1

    toc = time.perf_counter()
    print(f"Added {num_pairs} pairs in {toc - tic:0.4f} seconds.\n")
    return router
