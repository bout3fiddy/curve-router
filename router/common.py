import datetime
import typing
from dataclasses import dataclass


class BasePool(typing.NamedTuple):
    """A dataclass cacheing basepool lp token and coins in the base pool"""

    pool_address: str
    lp_token: str
    lp_token_decimals: int
    network: str
    coins: typing.List[str]


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


@dataclass(frozen=True)
class BestRoute:

    last_updated: datetime.datetime
    route: typing.List[Swap]
    coin_in: str
    coin_out: str


@dataclass(frozen=True)
class Wrapper(Swap):

    wrap: bool
    is_wrapper: bool = True
