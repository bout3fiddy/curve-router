from brownie_tokens import MintableForkToken

from router.curve_router import get_route
from router.swaps_integrator import convert_route_to_swaps_input


def test_3crv_to_cvxcrv_swap(router_mainnet, registry_swap, alice):

    coin_a = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490"
    coin_b = "0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7"
    amount_in = int(1E20)

    route = get_route(
        coin_in=coin_a,
        coin_out=coin_b,
        path_finder=router_mainnet,
        max_hops=4,
        max_shortest_paths=2,
        verbose=True,
    )

    assert len(route) > 0  # there should be a route possible

    swaps_input = convert_route_to_swaps_input(route)
    expected_swap_output = registry_swap.get_exchange_multiple_amount(
        swaps_input["_route"],
        swaps_input["_swap_params"],
        amount_in,
        swaps_input["_pools"]
    )

    assert expected_swap_output > 0

    threecrv = MintableForkToken(coin_a)
    threecrv._mint_for_testing(alice, amount_in)
    threecrv.approve(registry_swap, amount_in, {"from": alice})
    tx = registry_swap.exchange_multiple(
        swaps_input["_route"],
        swaps_input["_swap_params"],
        amount_in,
        int(expected_swap_output * 0.99),  # 1% slippage tolerance
        swaps_input["_pools"],
        {"from": alice}
    )

    assert tx.return_value > 0
    assert (tx.return_value - expected_swap_output)/expected_swap_output < 0.1



