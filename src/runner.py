import click
import json

from src.construct_coin_map import compile_graph
from src.core.common import PathFinder


@click.option("--network_name", default="Mainnet", type=str)
@click.option("--max_pairs", default=1e6, type=int)
def main(network_name, max_pairs):

    path_finder: PathFinder = compile_graph(network_name=network_name)
    coin_pairs = list(path_finder.coin_map.coin_pair_pool.keys())
    all_routes = {}

    c = 0
    for (coin_a, coin_b) in coin_pairs:

        c += 1

        all_routes[(coin_a, coin_b)] = path_finder.get_route(
            coin_a, coin_b, max_hops=5, verbose=False
        )

        if c == max_pairs:
            break

    json.dump(
        all_routes,
        open("all_routes.json", "w"),
        sort_keys=True,
        indent="\t",
        separators=(",", ": "),
    )


if __name__ == "__main__":
    main()
