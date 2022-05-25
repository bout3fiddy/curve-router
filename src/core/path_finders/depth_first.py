import typing

from src.core.common import BasePool, Coin, PathFinder


class DepthFirstSearch(PathFinder):
    def __init__(
        self, coins: typing.List[str], base_pools: typing.List[BasePool]
    ):
        super().__init__(coins, base_pools)

    def get_route(
        self,
        coin_a: Coin,
        coin_b: Coin,
        max_hops: int = 5,
        verbose: bool = True,
    ) -> typing.List[typing.Dict[typing.Tuple[str, str], typing.Dict]]:

        if verbose:
            print(
                f"Pathfinding for coins between "
                f"{coin_a.address} -> {coin_b.address}"
            )

        coin_paths = self._depth_first_search(coin_a, coin_b, [])

        # construct the swap route for coin pair
        all_coin_routes = []
        for coin_path in coin_paths:

            coin_pairs_in_path = list(zip(coin_path, coin_path[1:]))
            coin_pair_addresses = [
                (i.address, j.address) for (i, j) in coin_pairs_in_path
            ]

            constructed_swap_route = {
                coin_pair: self.coin_map.coin_pair_pool[coin_pair].__dict__
                for coin_pair in coin_pair_addresses
            }

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
    ):

        path = path + [coin_to_sell]

        if coin_to_sell == target_coin_to_buy:
            return [path]

        if coin_to_sell not in self.coin_map.coin_pairs.keys():
            return []

        if len(path) > max_hops:
            return []

        paths = []
        for (coin, pool) in self.coin_map.coin_pairs[coin_to_sell]:
            if coin not in path:
                paths.extend(
                    self._depth_first_search(coin, target_coin_to_buy, path)
                )

        return paths
