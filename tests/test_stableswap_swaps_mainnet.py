from router.curve_router import get_route


def test_3crv_to_cvxcrv_swap(router_mainnet):

    least_illiquid_route = get_route(
        coin_in="0x6c3f90f043a72fa612cbac8115ee7e52bde6e490",
        coin_out="0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7",
        path_finder=router_mainnet,
        max_hops=4,
        max_shortest_paths=2,
        verbose=True,
    )

    assert len(least_illiquid_route) > 0  # there should be a route possible
