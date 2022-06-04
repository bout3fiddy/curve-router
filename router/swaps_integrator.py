# Integrates router output to Swaps.vy input format for easier integration.
import typing

from brownie import ZERO_ADDRESS

from router.curve_router import get_route, initialise

MAX_HOPS = 4


def get_swap_type(
    is_stableswap: bool,
    num_coins_in_pool: int,  # todo: add num coins in pool here
    is_metapool: bool,
    is_lending_pool: bool,
    is_underlying_swap: bool,
    is_add_liquidity: bool,
    is_remove_liquidity: bool,
    is_cryptoswap: bool,
    is_poly_meta_zap: bool,
    network: str = "Mainnet"
):

    swap_type = 0
    is_add_remove_liquidity = is_add_liquidity or is_remove_liquidity
    is_pure_exchange = not (is_underlying_swap or is_add_remove_liquidity)

    # swap_type is 1. applicable to stableswap `exchange` method.
    if is_stableswap and is_pure_exchange:
        swap_type = 1

    elif is_stableswap and is_underlying_swap:
        swap_type = 2

    elif is_cryptoswap and is_pure_exchange:
        swap_type = 3

    elif is_cryptoswap and is_underlying_swap:
        swap_type = 4

    elif (
            network == "Matic" and
            is_metapool and
            is_stableswap and
            is_underlying_swap and
            is_poly_meta_zap
    ):
        swap_type = 5

    elif is_stableswap and is_add_liquidity and num_coins_in_pool == 2:
        swap_type = 6

    elif is_stableswap and is_add_liquidity and num_coins_in_pool == 3:
        swap_type = 7

    elif (
            is_stableswap and
            is_add_liquidity and
            is_lending_pool and
            network == "Matic"
    ):
        swap_type = 8

    elif is_stableswap and is_remove_liquidity:
        swap_type = 9

    elif (
            is_stableswap and
            is_remove_liquidity and
            is_lending_pool and
            network == "Matic"
    ):
        swap_type = 10

    return swap_type


def convert_route_to_swaps_input(
    curve_router_output: typing.List[typing.Dict],
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
    if not curve_router_output:
        raise "No routes in router output!"

    # initialise output dict
    swaps_input = {
        "_route": [curve_router_output[0]["coin_a"]],
        "_swap_params": [],
        "_pools": [],
    }
    for hop in curve_router_output:

        # get _route input:
        swaps_input["_route"].append(hop["pool"])
        swaps_input["_route"].append(hop["coin_b"])

        # get _swap_params:
        i = hop["i"]
        j = hop["j"]
        swap_type = get_swap_type(
            is_stableswap=hop["is_stableswap"] == "true",
            is_add_liquidity=hop["is_add_liquidity"] == "true",
            is_remove_liquidity=hop["is_remove_liquidity"] == "true",
            is_metapool=hop["is_metapool"] == "true",
            is_cryptoswap=hop["is_cryptoswap"] == "true",
            is_lending_pool=hop["is_lending_pool"] == "true",
            is_underlying_swap=hop["is_underlying_swap"] == "true",
        )
        swaps_input["_swap_params"].append([i, j, swap_type])

        # todo: get _pools for swaps via zap contracts

    # pad with ZERO_ADDRESS:
    swaps_input["_route"] += [ZERO_ADDRESS] * (
        MAX_HOPS * 2 + 1 - len(swaps_input["_route"])
    )
    swaps_input["_swap_params"] += [0, 0, 0] * (
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

    convert_route_to_swaps_input(least_illiquid_route)


if __name__ == "__main__":
    main()
