# @version 0.3.3
"""
@title Curve Router Contract
@license MIT
"""

interface StableSwap:
    def get_dy(i: int128, j: int128, dx: uint256) -> uint256: view
    def get_dy_underlying(i: int128, j: int128, dx: uint256) -> uint256: view


interface CryptoSwap:
    def get_dy(i: uint256, j: uint256, dx: uint256) -> uint256: view


interface WETH:
    def deposit(): payable
    def withdraw(_amount: uint256): nonpayable


@external
def __init__():

    pass


@external
@view
def get_dy_route(
    dx: uint256,
    pool_addresses: address[10],
    i: uint256[10],
    j: uint256[10],
    is_cryptoswap: bool[10],
    is_underlying_swap: bool[10],
    is_wrapper: bool[10],
) -> uint256:

    dy: uint256 = dx
    for route_idx in range(10):

        if pool_addresses[route_idx] == ZERO_ADDRESS:
            break

        # if a step involves wrapping or unwrapping, dy_idx == dx_idx
        # so we can just continue
        if is_wrapper[route_idx]:
            continue

        # stableswap swaps:
        if is_underlying_swap[route_idx] and not is_cryptoswap[route_idx]:
            dy = StableSwap(pool_addresses[route_idx]).get_dy_underlying(
                convert(i[route_idx], int128), convert(j[route_idx], int128), dy
            )
            continue

        if not is_cryptoswap[route_idx] and not is_underlying_swap[route_idx]:
            dy = StableSwap(pool_addresses[route_idx]).get_dy(
                convert(i[route_idx], int128), convert(j[route_idx], int128), dy
            )
            continue

        # cryptoswap swaps:
        if is_cryptoswap[route_idx] and not is_underlying_swap[route_idx]:
            dy = CryptoSwap(pool_addresses[route_idx]).get_dy(i[route_idx], j[route_idx], dy)
            continue

    return dy
