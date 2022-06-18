from brownie_tokens import MintableForkToken

from router.base_pools import USDT
from router.constants import CRV, CVX, ETH, EURT, THREECRV_ADDR, cvxCRV, WBTC
from router.curve_router import get_route
from router.swaps_integrator import convert_route_to_swaps_input


def test_swap_pairs_mainnet(router_mainnet, registry_swap, alice):

    pair = [
        (THREECRV_ADDR, cvxCRV),
        (CRV, CVX),
        (EURT, USDT),  # best path should have one hop with `swap_type` == 4
        (ETH, WBTC)  # best path should be one hop on tricrypto2
    ]
    amount_in = int(1e20)
    for (coin_a, coin_b) in pair:
        route = get_route(
            coin_in=coin_a,
            coin_out=coin_b,
            path_finder=router_mainnet,
            max_hops=4,
            max_shortest_paths=2,
            verbose=True,
        )

        assert len(route) > 0

        if coin_a == EURT:
            assert len(route) == 1  # should have one rout with swap_type == 4

        if coin_a == ETH and coin_b == WBTC:
            assert len(route) == 1

        swaps_input = convert_route_to_swaps_input(route)
        expected = registry_swap.get_exchange_multiple_amount(
            swaps_input["_route"],
            swaps_input["_swap_params"],
            amount_in,
            swaps_input["_pools"],
        )

        assert expected > 0

        coin_a_forktoken = MintableForkToken(coin_a)
        coin_b_forktoken = MintableForkToken(coin_b)
        coin_a_forktoken._mint_for_testing(alice, amount_in)
        coin_a_forktoken.approve(registry_swap, amount_in, {"from": alice})

        initial_coin_b_balance = coin_b_forktoken.balanceOf(alice)
        tx = registry_swap.exchange_multiple(
            swaps_input["_route"],
            swaps_input["_swap_params"],
            amount_in,
            int(expected * 0.99),  # 1% slippage tolerance
            swaps_input["_pools"],
            {"from": alice},
        )
        assert tx.return_value > 0
        assert abs(expected - tx.return_value) / expected < 0.1
        assert coin_b_forktoken.balanceOf(alice) != initial_coin_b_balance
