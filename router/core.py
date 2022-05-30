import typing
from datetime import datetime

from router.common import Swap


class Router:
    last_updated: int = 0

    def __init__(self, coins: typing.List[str]):
        self.coin_map = CoinMap(coins)

    def get_routes(
        self,
        coin_a: str,
        coin_b: str,
        max_hops: int = 5,
    ) -> typing.Dict[int, typing.List[typing.Dict]]:
        """_summary_

        Args:
            coin_a (str): _description_
            coin_b (str): _description_
            max_hops (int, optional): _description_. Defaults to 5.

        Raises:
            ValueError: _description_

        Returns:
            typing.List[typing.List[typing.Dict]]: _description_
        """

        coin_paths = self._depth_first_search(
            coin_a, coin_b, [], None, max_hops
        )

        # construct the swap route for coin pair:
        all_coin_routes = {i: [] for i in range(max_hops+1)}
        for coin_path in coin_paths:
            if len(coin_path) > max_hops:
                continue
            all_coin_routes[len(coin_path)].append(
                [swap.__dict__ for swap in coin_path]
            )

        return all_coin_routes

    def _depth_first_search(
        self,
        coin_to_sell: str,
        target_coin_to_buy: str,
        path: typing.List,
        swap: typing.Optional[Swap] = None,
        max_hops: int = 5,
    ) -> typing.List:
        """_summary_

        Inspiration: https://stackabuse.com/depth-first-search-dfs-in-python-theory-and-implementation/

        Args:
            coin_to_sell (str): _description_
            target_coin_to_buy (str): _description_
            path (typing.List): _description_
            max_hops (int, optional): _description_. Defaults to 5.

        Returns:
            typing.List: _description_
        """
        if swap:
            path = path + [swap]

        if coin_to_sell == target_coin_to_buy:
            return [path]

        if coin_to_sell not in self.coin_map.mapping.keys():
            return []

        if len(path) > max_hops:
            return []

        # recursion here:
        paths = []
        for (coin, swap) in self.coin_map.mapping[coin_to_sell]:
            if coin not in path:
                paths.extend(
                    self._depth_first_search(
                        coin, target_coin_to_buy, path, swap, max_hops
                    )
                )

        return paths


class CoinMap:
    last_updated: datetime

    def __init__(self, coins: typing.List[str]):

        self.mapping = {coin: [] for coin in coins}
        self.coin_pairs = {}

    def add_pair(self, coin_a: str, coin_b: str, swap: Swap):

        if coin_a not in self.mapping.keys():
            self.mapping[coin_a] = []

        if (coin_a, coin_b) not in self.coin_pairs.keys():
            self.coin_pairs[(coin_a, coin_b)] = []

        self.mapping[coin_a].append((coin_b, swap))
        self.coin_pairs[(coin_a, coin_b)].append(swap)

        self.last_updated = datetime.utcnow()
