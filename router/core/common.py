import typing
from abc import abstractmethod
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

    is_wrapper: bool = True
    wrap: bool


class CoinMap:
    def __init__(self, coins: typing.List[str]):

        self.number_of_coins = len(coins)
        self.coins = coins
        self.mapping = {coin: set() for coin in coins}
        self.coin_pairs = {}

    def add_pair(self, coin_a: Coin, coin_b: Coin, swap: Swap):

        if coin_a not in self.mapping.keys():
            self.mapping[coin_a] = set()

        self.mapping[coin_a].add((coin_b, swap))
        self.coin_pairs[(coin_a, coin_b)] = swap


class PathFinder:
    def __init__(self, coins: typing.List[str]):
        self.coin_map = CoinMap(coins)

    @abstractmethod
    def get_routes(
        self,
        coin_a: Coin,
        coin_b: Coin,
        max_hops: int = 5,
    ) -> typing.List[typing.List[typing.Dict]]:
        raise NotImplementedError
