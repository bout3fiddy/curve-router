from abc import abstractmethod
from dataclasses import dataclass
import typing


# ------------ Core DataClasses ------------ #


class Coin(typing.NamedTuple):
    """A dataclass cacheing some coin info and a few basic methods."""

    address: str
    network: str
    decimals: int


class BasePool(typing.NamedTuple):
    """A dataclass cacheing basepool lp token and coins in the base pool"""

    pool_address: str
    lp_token: Coin
    lp_token_decimals: int
    network: str
    coins: typing.List[Coin]


@dataclass(eq=True, frozen=True)
class Pool:
    """A dataclass containing details on the pool connecting two assets"""

    address: str
    network: str
    coin_a: Coin
    coin_b: Coin


# ------------ Core CoinMap ------------ #


class CoinMap:
    def __init__(
        self, coins: typing.List[str], base_pools: typing.List[BasePool]
    ):

        self.number_of_coins = len(coins)
        self.coins = coins
        self.coin_pairs = {coin: set() for coin in coins}
        self.coin_pair_pool = {}
        self.base_pools = base_pools

    def add_pair(self, coin_a: Coin, coin_b: Coin, pool: Pool):

        if coin_a not in self.coin_pairs.keys():
            self.coin_pairs[coin_a] = set()

        self.coin_pairs[coin_a].add((coin_b, pool))
        self.coin_pair_pool[(coin_a.address, coin_b.address)] = pool


class PathFinder:
    def __init__(
        self, coins: typing.List[str], base_pools: typing.List[BasePool]
    ):

        self.coin_map = CoinMap(coins, base_pools)

    @abstractmethod
    def get_route(
        self,
        coin_a: Coin,
        coin_b: Coin,
        max_hops: int = 5,
        verbose: bool = True,
    ) -> typing.List[typing.Dict[typing.Tuple[str, str], typing.Dict]]:
        raise NotImplementedError

    def print_route(self, coin_a: Coin, coin_b: Coin, max_hops: int = 5):
        all_routes = self.get_route(coin_a, coin_b, max_hops)

        c = 1
        for route in all_routes:
            print(f"Route #{c}")
            c += 1
            for pair, pool in route.items():
                print(
                    f"Coin in: {pair[0]} -> Pool: {pair[1]} -> "
                    f"Coin out: {pool['address']}\n"
                )
            print("\n")
