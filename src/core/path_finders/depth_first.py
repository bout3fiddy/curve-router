import typing
from core.common import Route, Coin, BasePool, Pool, CoinMap


class DepthFirstSearch(CoinMap):
    def __init__(self, coins: typing.List[str], base_pools: typing.List[BasePool]):

        super().__init_(coins)
        self.base_pools = base_pools

    def get_route(
        self, coin_a: Coin, coin_b: Coin, max_hops: int = 5, verbose: bool = True
    ) -> typing.List[Route]:

        if verbose:
            print(f"Pathfinding for coins between {coin_a.address} -> {coin_b.address}")

        # hack to reduce graph size: usdt, usdc and dai are just threecrv in this search space
        for base_pool_data in self.base_pools:
            if coin_a in base_pool_data.coins:
                coin_a = base_pool_data.lp_token
                if verbose:
                    print(
                        f"Coin in basepool. Searching for coins between {coin_a} -> {coin_b} instead."
                    )

            if coin_b in base_pool_data.coins:
                coin_b = base_pool_data.lp_token
                if verbose:
                    print(
                        f"Coin in basepool. Searching for coins between {coin_a} -> {coin_b} instead."
                    )

        coin_paths = self._depth_first_search(coin_a, coin_b)

        # construct the swap route for coin pair
        all_coin_routes = []
        for coin_path in coin_paths:
            coin_pairs_in_path = list(zip(coin_path, coin_path[1:]))
            constructed_swap_route = [
                self.coin_pair_pool[coin_pair] for coin_pair in coin_pairs_in_path
            ]

            if len(constructed_swap_route) > max_hops:
                continue

            coin_route = Route(
                coin_a=coin_a,
                coin_b=coin_b,
                n_hops=len(constructed_swap_route),
                pools=constructed_swap_route,
            )

            if not coin_route in all_coin_routes:
                all_coin_routes.append(coin_route)

        return all_coin_routes

    def _depth_first_search(
        self,
        coin_to_sell: Coin,
        target_coin_to_buy: Coin,
        path: typing.List = [],
        max_hops: int = 5,
    ):

        path = path + [coin_to_sell]

        if coin_to_sell == target_coin_to_buy:
            return [path]

        if coin_to_sell not in self.coin_pairs.keys():
            return []

        if len(path) > max_hops:
            return []

        paths = []
        for (coin, pool) in self.coin_pairs[coin_to_sell]:
            if coin not in path:
                paths.extend(self._depth_first_search(coin, target_coin_to_buy, path))

        return paths
