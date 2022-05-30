import json
import click

from router.coins import THREECRV_BASEPOOL
from router.construct_coin_map import init_router
from utils.misc import Timer


@click.command()
@click.option("--coin_in", type=str)
@click.option("--coin_out", type=str)
@click.option("--network_name", default="Mainnet", type=str)
@click.option("--max_hops", type=int, default=5)
@click.option("--max_shortest_paths", type=int, default=2)
def main(coin_in, coin_out, network_name, max_hops, max_shortest_paths):

    coin_in = coin_in.lower()
    coin_out = coin_out.lower()

    # compile graph:
    path_finder = init_router(
        network_name=network_name, base_pools=[THREECRV_BASEPOOL]
    )
    print("Graph compiled.")

    # find all routes between coin_a and coin_b:
    print(f"Finding routes for {coin_in} -> {coin_out}.")
    with Timer() as t:
        routes = path_finder.get_routes(coin_in, coin_out, max_hops=max_hops)
    print(f"Found routes in {t.interval:0.4f} seconds.\n")

    # select all routes for two shortest hops
    pruned_routes = []
    c = -1
    for n_hop, routes_for_n_hops in routes.items():
        c += 1
        if len(routes_for_n_hops) == 0:
            continue
        if c > max_shortest_paths:
            break
        pruned_routes.extend(routes_for_n_hops)
    print(f"Selecting {len(pruned_routes)} routes for the next step.\n")

    # dump all routes in json file:
    json.dump(
        pruned_routes,
        open(f"routes_{network_name}_{coin_in}_{coin_out}.json", "w"),
        sort_keys=True,
        indent="\t",
        separators=(",", ": "),
    )


if __name__ == "__main__":
    main()
