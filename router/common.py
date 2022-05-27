import typing
from dataclasses import dataclass


class Coin(typing.NamedTuple):
    """A dataclass cacheing some coin info and a few basic methods."""

    address: str
    network: str
    decimals: int
    is_lp_token: bool = False


class BasePool(typing.NamedTuple):
    """A dataclass cacheing basepool lp token and coins in the base pool"""

    pool_address: str
    lp_token: Coin
    lp_token_decimals: int
    network: str
    coins: typing.List[Coin]


@dataclass(frozen=True)
class Swap:
    """A dataclass containing details on the pool connecting two assets"""

    pool: str  # address
    network: str
    is_cryptoswap: bool
    is_stableswap: bool
    is_metapool: bool
    base_pool: str  # address
    is_underlying_swap: bool
    i: int  # coin to swap from
    j: int  # coin to swap to
    coin_a: str  # address
    coin_b: str  # address
    coin_a_decimals: int
    coin_b_decimals: int


@dataclass(frozen=True)
class Wrapper(Swap):

    wrap: bool
    is_wrapper: bool = True
