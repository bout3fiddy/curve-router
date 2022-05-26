from brownie import Contract


def test_swap_route_one_hop(curve_router, route_one_hop):

    dx = 10**18
    dy = curve_router.get_dy_route(
        dx,
        route_one_hop["pool_addresses"],
        route_one_hop["i"],
        route_one_hop["j"],
        route_one_hop["is_cryptoswap"],
        route_one_hop["is_underlying_swap"],
        route_one_hop["is_wrapper"],
    )

    pool = Contract.from_explorer(route_one_hop["pool_addresses"][0])
    dy_actual = pool.get_dy(0, 1, dx)

    assert dy == dy_actual
