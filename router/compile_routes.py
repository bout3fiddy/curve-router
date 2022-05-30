import json
import time

import click

from router.coins import THREECRV_BASEPOOL
from router.construct_coin_map import init_router


@click.command()
@click.option("--network_name", default="Mainnet", type=str)
@click.option("--max_pairs", default=1e6, type=int)
def main(network_name, max_pairs):

    path_finder = init_router(
        network_name=network_name, base_pools=[THREECRV_BASEPOOL]
    )
    print("Graph is compiled.")
    coin_pairs = path_finder.coin_map.coin_pairs
    all_routes = {}

    c = 0
    for (coin_a, coin_b) in coin_pairs:

        print(f"coin pairs left: {len(coin_pairs) - c}.")
        print(f"Finding routes for {coin_a} -> {coin_b}.")

        tic = time.perf_counter()
        routes = path_finder.get_routes(coin_a, coin_b, max_hops=5)
        toc = time.perf_counter()
        print(f"Found {len(routes)} routes in {toc - tic:0.4f} seconds.\n")

        all_routes[f"{coin_a.address} -> {coin_b.address}"] = routes

        if len(routes) > 10:
            print("Too many routes?")

        c += 1
        if c == max_pairs:
            break

    json.dump(
        all_routes,
        open(f"all_routes_{network_name}.json", "w"),
        sort_keys=True,
        indent="\t",
        separators=(",", ": "),
    )


if __name__ == "__main__":
    main()
