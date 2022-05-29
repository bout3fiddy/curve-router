import json
import click

from router.coins import THREECRV_BASEPOOL
from router.construct_coin_map import init_router
from utils.misc import Timer


@click.command()
@click.option("--network_name", default="Mainnet", type=str)
@click.option("--coin_in", type=str)
@click.option("--coin_out", type=str)
@click.option("--max_routes", type=int, default=10)
def main(network_name, coin_in, coin_out, max_routes):

    coin_in = coin_in.lower()
    coin_out = coin_out.lower()

    # compile graph:
    path_finder = init_router(
        network_name=network_name, base_pools=[THREECRV_BASEPOOL]
    )
    print("Graph is compiled.")

    # find all routes between coin_a and coin_b:
    print(f"Finding routes for {coin_in} -> {coin_out}.")
    with Timer() as t:
        routes = path_finder.get_routes(coin_in, coin_out, max_hops=5)
    print(f"Found {len(routes)} routes in {t.interval:0.4f} seconds.\n")

    # arrange routes by length and select the first `max_hop` routes
    n_hops = [len(route) for route in routes]
    min_hops = min(n_hops)
    max_hops = max(n_hops)
    swap_hops_distribution = {
        i: sum(
            [1 if len(route) == i else 0 for route in routes]
        ) for i in list(set(n_hops))
    }

    # dump all routes in json file:
    json.dump(
        routes,
        open(f"routes_{network_name}_{coin_in}_{coin_out}.json", "w"),
        sort_keys=True,
        indent="\t",
        separators=(",", ": "),
    )


if __name__ == "__main__":
    main()
