import json

import click
from utils.misc import Timer

from router.coins import THREECRV_BASEPOOL
from router.construct_coin_map import init_router


@click.command()
@click.option("--coin_in", type=str)
@click.option("--coin_out", type=str)
@click.option("--network_name", default="Mainnet", type=str)
@click.option("--max_hops", type=int, default=5)
@click.option("--max_shortest_paths", type=int, default=2)
def main(coin_in, coin_out, network_name, max_hops, max_shortest_paths):

    coin_in = coin_in.lower()
    coin_out = coin_out.lower()

    print("Initialising path finder's coin map ...")
    # compile graph:
    with Timer() as t:
        path_finder = init_router(
            network_name=network_name, base_pools=[THREECRV_BASEPOOL]
        )
    print(f"Path Finder coin map initialised. Took: {t.interval:0.4f} seconds.")

    # find all routes between coin_a and coin_b:
    print(f"Finding routes for {coin_in} -> {coin_out}.")
    with Timer() as t:
        routes = path_finder.get_routes(coin_in, coin_out, max_hops=max_hops)
    num_routes_found = sum(
        [len(routes_for_hops) for n_hops, routes_for_hops in routes.items()]
    )
    print(f"Found {num_routes_found} routes in {t.interval:0.4f} seconds.")

    # select all routes for two shortest hops
    with Timer() as t:
        pruned_routes = []
        c = -1
        for n_hop, routes_for_n_hops in routes.items():
            c += 1
            if len(routes_for_n_hops) == 0:
                continue
            if c > max_shortest_paths:
                break
            pruned_routes.extend(routes_for_n_hops)
    print(
        f"Selecting {len(pruned_routes)} routes for the next step. "
        f"Took {t.interval} seconds."
    )

    # remove all hops (greater than 1 swap) where any pool has been re-visited:
    print("Removing all routes where a pool was re-visited ...")
    with Timer() as t:
        non_redundant_hops = []
        for route in pruned_routes:
            pools_in_route = [swap['pool'] for swap in route]
            if len(list(set(pools_in_route))) != len(pools_in_route):
                continue
            non_redundant_hops.append(route)
    print(
        f"Num pools selected: {len(non_redundant_hops)}. "
        f"Run took: {t.interval:.04f} seconds."
    )

    # dump all routes in json file:
    json.dump(
        non_redundant_hops,
        open(f"routes_{network_name}_{coin_in}_{coin_out}.json", "w"),
        sort_keys=True,
        indent="\t",
        separators=(",", ": "),
    )


if __name__ == "__main__":
    main()

