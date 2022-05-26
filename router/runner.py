import json

import click

from router.construct_coin_map import compile_graph
from router.core.coins import THREECRV_BASEPOOL


@click.command()
@click.option("--network_name", default="Mainnet", type=str)
@click.option("--max_pairs", default=1e6, type=int)
def main(network_name, max_pairs):

    path_finder = compile_graph(
        network_name=network_name, base_pools=[THREECRV_BASEPOOL]
    )
    coin_pairs = path_finder.coin_map.coin_pairs
    all_routes = {}

    c = 0
    for (coin_a, coin_b) in coin_pairs:

        c += 1

        all_routes[f"{coin_a.address} -> {coin_b.address}"] = path_finder.get_routes(
            coin_a, coin_b, max_hops=5
        )

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
