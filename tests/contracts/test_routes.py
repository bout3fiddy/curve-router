from brownie import Contract


def test_swap_route_one_hop(route_one_hop, curve_router):

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


def test_rai_ageur_swap(route_rai_ageur, curve_router):

    dx = 10**18
    dy = curve_router.get_dy_route(
        dx,
        route_rai_ageur["pool_addresses"],
        route_rai_ageur["i"],
        route_rai_ageur["j"],
        route_rai_ageur["is_cryptoswap"],
        route_rai_ageur["is_underlying_swap"],
        route_rai_ageur["is_wrapper"],
    )

    print(dx, dy)

    assert 0 > 1
