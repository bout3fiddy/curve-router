import json
import pprint

import click

from router.base_pools import BASE_POOLS
from router.construct_coin_map import init_router
from router.core import Router
from router.misc import Timer


def print_verbose(statement: str, verbose: bool = True):
    if verbose:
        print(statement)


def initialise(network_name: str, verbose: bool = False) -> Router:
    print_verbose("Initialising path finder's coin map ...\n", verbose)
    path_finder = init_router(
        network_name=network_name, base_pools=BASE_POOLS[network_name]
    )
    print_verbose("Path Finder coin map initialised.", verbose)
    return path_finder


def get_route(
    coin_in: str,
    coin_out: str,
    path_finder: Router,
    max_hops: int = 5,
    max_shortest_paths: int = 2,
    verbose: bool = False,
):

    coin_in = coin_in.lower()
    coin_out = coin_out.lower()

    # find all routes between coin_a and coin_b:
    print_verbose(f"Finding routes for {coin_in} -> {coin_out}.", verbose)
    with Timer() as t:
        routes = path_finder.get_routes(coin_in, coin_out, max_hops=max_hops)
    num_routes_found = sum(
        [len(routes_for_hops) for n_hops, routes_for_hops in routes.items()]
    )
    print_verbose(
        f"Found {num_routes_found} routes in {t.interval:0.4f} seconds.",
        verbose,
    )

    # select all routes for two shortest hops
    with Timer() as t:
        pruned_routes = []
        c = 0
        for n_hop, routes_for_n_hops in routes.items():
            if len(routes_for_n_hops) == 0:
                continue
            if c > max_shortest_paths:
                break
            pruned_routes.extend(routes_for_n_hops)
            c += 1
    print_verbose(
        f"Selecting {len(pruned_routes)} routes for the next step. "
        f"Took {t.interval} seconds.",
        verbose,
    )

    # remove all hops where any pool has been re-visited:
    print_verbose(
        "Removing all routes where a pool was re-visited ...", verbose
    )
    with Timer() as t:
        non_redundant_hops = []
        for route in pruned_routes:
            pools_in_route = [swap["pool"] for swap in route]
            if len(list(set(pools_in_route))) != len(pools_in_route):
                continue
            non_redundant_hops.append(route)
    print_verbose(
        f"Num pools selected: {len(non_redundant_hops)}. "
        f"Run took: {t.interval:.04f} seconds.",
        verbose,
    )

    # Select the route with the highest average liquidity. This is a proxy for
    # minimising slippage:
    min_route_liquidity = []
    for route in non_redundant_hops:
        route_liquidity = [swap["pool_tvl_usd"] for swap in route]
        min_route_liquidity.append(min(route_liquidity))

    least_illiquid_route = non_redundant_hops[
        min_route_liquidity.index(max(min_route_liquidity))
    ]

    return least_illiquid_route


@click.command()
@click.option("--coin_in", type=str)
@click.option("--coin_out", type=str)
@click.option("--network_name", default="Mainnet", type=str)
@click.option("--max_hops", type=int, default=5)
@click.option("--max_shortest_paths", type=int, default=2)
@click.option("--write_to_json", type=bool, default=True)
def main(
    coin_in,
    coin_out,
    network_name,
    max_hops,
    max_shortest_paths,
    write_to_json,
):
    # initialise coin map:
    path_finder = initialise(network_name)

    least_illiquid_route = get_route(
        coin_in=coin_in,
        coin_out=coin_out,
        path_finder=path_finder,
        max_hops=max_hops,
        max_shortest_paths=max_shortest_paths,
        verbose=True,
    )

    print("Found least illiquid route:")
    pprint.pprint(least_illiquid_route, indent=True)

    # dump all routes in json file:
    if write_to_json:
        json.dump(
            least_illiquid_route,
            open(f"routes_{network_name}_{coin_in}_{coin_out}.json", "w"),
            sort_keys=True,
            indent="\t",
            separators=(",", ": "),
        )


if __name__ == "__main__":
    main()
