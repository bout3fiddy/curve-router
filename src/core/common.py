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


@dataclass
class Route:
    """A dataclass containing multi hops between coin a and coin b"""

    n_hops: int
    pools: typing.List[Pool]
    coin_a: str
    coin_b: str


# ------------ Core CoinMap ------------ #


class CoinMap:
    def __init__(self, coins: typing.List[str]):

        self.number_of_coins = len(coins)
        self.coins = coins
        self.coin_pairs = {coin: set() for coin in coins}
        self.coin_pair_pool = {}

    def add_pair(self, coin_a: Coin, coin_b: Coin, pool: Pool):

        if coin_a not in self.coin_pairs.keys():
            self.coin_pairs[coin_a] = set()

        self.coin_pairs[coin_a].add((coin_b, pool))
        self.coin_pair_pool[(coin_a, coin_b)] = pool

    @abstractmethod
    def get_route(
        self, coin_a: Coin, coin_b: Coin, max_hops: int = 5, verbose: bool = True
    ) -> typing.List[Route]:
        raise NotImplementedError

    @abstractmethod
    def print_route(self, coin_a: Coin, coin_b: Coin, max_hops: int = 5):
        all_routes = self.get_route(coin_a, coin_b, max_hops)

        c = 1
        for route in all_routes:
            print(f"Route #{c}")
            c += 1
            for hops in route.pools:
                print(
                    f"Coin in: {hops.coin_a.address} -> Pool: {hops.address} -> Coin out: {hops.coin_b.address}\n"
                )
            print("\n")
