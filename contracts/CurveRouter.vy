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


@internal
@view
def _get_dy_stableswap(pool_address: address, dx: uint256, i: int128, j: int128, underlying: bool = False) -> uint256:

    if underlying:
        return StableSwap(pool_address).get_dy_underlying(i, j, dx)

    return StableSwap(pool_address).get_dy(i, j, dx)


@internal
@view
def _get_dy_cryptoswap(pool_address: address, dx: uint256, i: uint256, j: uint256) -> uint256:

    return CryptoSwap(pool_address).get_dy(i, j, dx)


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

    dy: uint256 = 0
    _dx: uint256 = dx

    for idx in range(10):        

        if pool_addresses[idx] == ZERO_ADDRESS:
            break

        # if a step involves wrapping or unwrapping, dy = dx
        # so we can just continue
        if is_wrapper[idx]:
            continue

        # stableswap swaps:
        if not is_cryptoswap[idx]:
            i_int: int128 = convert(i[idx], int128)
            j_int: int128 = convert(j[idx], int128)
            dy = self._get_dy_stableswap(pool_addresses[idx], _dx, i_int, j_int, is_underlying_swap[idx])

        elif is_cryptoswap[idx]:
            dy = self._get_dy_cryptoswap(pool_addresses[idx], _dx, i[idx], j[idx])
        
        _dx = dy

    return dy
