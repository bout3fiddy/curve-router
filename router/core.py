import typing

from router.common import Coin, CoinMap


class Router:
    def __init__(self, coins: typing.List[str]):
        self.coin_map = CoinMap(coins)

    def get_routes(
        self,
        coin_a: Coin,
        coin_b: Coin,
        max_hops: int = 5,
    ) -> typing.List[typing.List[typing.Dict]]:
        """_summary_

        Args:
            coin_a (Coin): _description_
            coin_b (Coin): _description_
            max_hops (int, optional): _description_. Defaults to 5.

        Raises:
            ValueError: _description_

        Returns:
            typing.List[typing.List[typing.Dict]]: _description_
        """

        coin_paths = self._depth_first_search(coin_a, coin_b, [])

        # construct the swap route for coin pair:
        all_coin_routes = []
        for coin_path in coin_paths:

            coin_pairs_in_path = list(zip(coin_path, coin_path[1:]))
            constructed_swap_route = [
                self.coin_map.coin_pairs[coin_pair].__dict__
                for coin_pair in coin_pairs_in_path
            ]

            if len(constructed_swap_route) > max_hops:
                continue

            if constructed_swap_route not in all_coin_routes:
                all_coin_routes.append(constructed_swap_route)

        return all_coin_routes

    def _depth_first_search(
        self,
        coin_to_sell: Coin,
        target_coin_to_buy: Coin,
        path: typing.List,
        max_hops: int = 5,
    ) -> typing.List:
        """_summary_

        Inspiration: https://stackabuse.com/depth-first-search-dfs-in-python-theory-and-implementation/

        Args:
            coin_to_sell (Coin): _description_
            target_coin_to_buy (Coin): _description_
            path (typing.List): _description_
            max_hops (int, optional): _description_. Defaults to 5.

        Returns:
            typing.List: _description_
        """

        path = path + [coin_to_sell]

        if coin_to_sell == target_coin_to_buy:
            return [path]

        if coin_to_sell not in self.coin_map.mapping.keys():
            return []

        if len(path) > max_hops:
            return []

        paths = []
        for (coin, pool) in self.coin_map.mapping[coin_to_sell]:
            if coin not in path:
                paths.extend(
                    self._depth_first_search(coin, target_coin_to_buy, path)
                )

        return paths
