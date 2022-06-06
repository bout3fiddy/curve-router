# Integrates router output to Swaps.vy input format for easier integration.
import typing

from brownie import ZERO_ADDRESS

from router.constants import TRICRYPTO2
from router.curve_router import get_route, initialise

MAX_HOPS = 4


def get_swap_type(
    is_stableswap: bool,
    num_coins_in_pool: int,  # todo: add num coins in pool here
    is_metapool: bool,
    is_underlying: bool,
    is_add_liquidity: bool,
    is_remove_liquidity: bool,
    is_cryptoswap: bool,
    is_poly_meta_zap: bool,
):

    swap_type = 0
    is_add_remove_liquidity = is_add_liquidity or is_remove_liquidity
    is_pure_exchange = not (is_underlying or is_add_remove_liquidity)

    # swap_type is 1. applicable to stableswap `exchange` method.
    if is_stableswap and is_pure_exchange:
        swap_type = 1

    elif is_stableswap and is_underlying:
        swap_type = 2

    elif is_cryptoswap and is_pure_exchange:
        swap_type = 3

    # cryptoswap `exchange_underlying` method to swap using eth and not weth
    elif is_cryptoswap and is_underlying:
        # swap_type = 4
        swap_type = 3  # ignoring swap type 4 entirely

    elif is_metapool and is_stableswap and is_underlying and is_poly_meta_zap:
        swap_type = 5

    elif is_stableswap and is_add_liquidity and num_coins_in_pool == 2:
        swap_type = 6

    elif is_stableswap and is_add_liquidity and num_coins_in_pool == 3:
        swap_type = 7

    elif (
        is_stableswap
        and is_add_liquidity
        and num_coins_in_pool == 3
        and is_underlying
    ):
        swap_type = 8

    elif is_stableswap and is_remove_liquidity:
        swap_type = 9

    elif is_stableswap and is_remove_liquidity and is_underlying:
        swap_type = 10

    return swap_type


def convert_route_to_swaps_input(
    route: typing.List[typing.Dict],
) -> typing.Dict:
    """Takes curve_router.py output (list of dicts) to an input that is
    digestible by `exchange_multiple` method in Swaps.vy router contract.

    Input config for Swaps.vy:
    _route:         Array of [initial token, pool, token, pool, token, ...]
                    The array is iterated until a pool address of 0x00,
                    then the last given token is transferred to `_receiver`
    _swap_params:   Multidimensional array of [i, j, swap type] where
                    i and j are the correct values for the n'th pool in
                    `_route`.

                    The swap type should be:
                    1           -> a stableswap `exchange`
                    2           -> for stableswap `exchange_underlying`
                    3           -> for a cryptoswap `exchange`
                    4           -> for a cryptoswap `exchange_underlying`
                    5           -> for Polygon factory metapools
                                   `exchange_underlying`
                    6-8         -> for underlying coin > LP token "exchange"
                                   (actually `add_liquidity`),
                    9 and 10    -> for LP token > underlying coin "exchange"
                                   (actually `remove_liquidity_one_coin`)
    _amount:        The amount of `_route[0]` token being sent.
    _expected:      The minimum amount received after the final swap.
    _pools:         Array of pools for swaps via zap contracts. This parameter
                    is only needed for Polygon meta-factories underlying swaps.
    _receiver:      Address to transfer the final output token to.

    Note: max hops possible with Swaps.vy is 4.

    Output:
        Dict containing _route, _swap_params, _pools
    """
    if not route:
        raise "No routes in router output!"

    # initialise output dict
    swaps_input = {
        "_route": [route[0]["coin_a"]],
        "_swap_params": [],
        "_pools": [],
    }

    # If tricrypto2 in route, then use weth. else use eth
    # (via `exchange_underlying`):
    route_has_tricrypto2 = any(hop["pool"] == TRICRYPTO2 for hop in route)

    for hop in route:

        # get _route input:
        swaps_input["_route"].append(hop["pool"])
        swaps_input["_route"].append(hop["coin_b"])

        # get _swap_params:
        i = hop["i"]
        j = hop["j"]

        # if tricrypto is involved, the deal with weth. else eth.
        is_underlying = hop["is_underlying"]
        if route_has_tricrypto2 and hop["is_cryptoswap"]:
            is_underlying = False

        swap_type = get_swap_type(
            is_stableswap=hop["is_stableswap"],
            is_add_liquidity=hop["is_add_liquidity"],
            is_remove_liquidity=hop["is_remove_liquidity"],
            is_metapool=hop["is_metapool"],
            is_cryptoswap=hop["is_cryptoswap"],
            is_underlying=is_underlying,
            is_poly_meta_zap=hop["zap_address"] is not ZERO_ADDRESS,
            num_coins_in_pool=hop["num_coins_pool"],
        )
        swaps_input["_swap_params"].append([i, j, swap_type])

        # get _pool (zap address):
        swaps_input["_pools"].append(hop["zap_address"])

    # pad with ZERO_ADDRESS:
    swaps_input["_route"] += [ZERO_ADDRESS] * (
        MAX_HOPS * 2 + 1 - len(swaps_input["_route"])
    )
    swaps_input["_swap_params"] += [[0, 0, 0]] * (
        MAX_HOPS - len(swaps_input["_swap_params"])
    )
    swaps_input["_pools"] += [ZERO_ADDRESS] * (
        MAX_HOPS - len(swaps_input["_pools"])
    )

    return swaps_input


def main():
    # initialise coin map:
    router_mainnet = initialise("Mainnet")

    least_illiquid_route = get_route(
        coin_in="0x6c3f90f043a72fa612cbac8115ee7e52bde6e490",
        coin_out="0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7",
        path_finder=router_mainnet,
        max_hops=4,
        max_shortest_paths=2,
        verbose=True,
    )

    swaps_input = convert_route_to_swaps_input(least_illiquid_route)
    print(swaps_input)


if __name__ == "__main__":
    main()
