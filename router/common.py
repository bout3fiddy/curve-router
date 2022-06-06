import typing
from dataclasses import dataclass
from brownie import ZERO_ADDRESS


class BasePool(typing.NamedTuple):
    """A dataclass cacheing basepool lp token and coins in the base pool"""

    pool_address: str
    lp_token: str
    network: str
    coins: typing.List[str]  # if lending: underlying is e.g. aDAI or gDAI
    is_lending: bool = False
    is_cryptoswap: bool = False
    # if lending: underlying is e.g. DAI
    underlying_coins: typing.List[str] = []
    # if meta lending factory pool, then `exchange_underlying` yields aTokens
    # and not underlying_coins. So there exists a separate contract for
    # swaps, called the zap depositor.
    zap_address: str = ZERO_ADDRESS


@dataclass(frozen=True)
class Swap:
    """A dataclass containing details on the pool connecting two assets"""

    pool: str  # address
    network: str
    is_cryptoswap: bool
    is_stableswap: bool
    is_metapool: bool
    base_pool: str  # address
    is_underlying: bool
    i: int  # coin to swap from
    j: int  # coin to swap to
    coin_a: str  # address
    coin_b: str  # address
    pool_tvl_usd: float
    num_coins_pool: float
    is_lending_pool: bool = False
    is_add_liquidity: bool = False  # lp token to coin in basepool
    is_remove_liquidity: bool = False  # coin to lp token in basepool
    zap_address: str = ZERO_ADDRESS  # contract for meta factory lending pools
    use_eth: bool = True  # if cryptoswap then use eth and not weth
