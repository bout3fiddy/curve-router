import pytest
from brownie import ZERO_ADDRESS, CurveRouter, accounts


@pytest.fixture(scope="module")
def alice():
    return accounts[0]


@pytest.fixture(scope="module")
def curve_router(alice):
    return CurveRouter.deploy({"from": alice})


@pytest.fixture(scope="module")
def route_one_hop():
    pool_addresses = [ZERO_ADDRESS] * 10
    pool_addresses[0] = "0x01FE650EF2f8e2982295489AE6aDc1413bF6011F"
    i = [0] * 10
    j = [0] * 10
    j[0] = 1
    is_cryptoswap = [False] * 10
    is_underlying_swap = [False] * 10
    is_wrapper = [False] * 10

    return {
        "pool_addresses": pool_addresses,
        "i": i,
        "j": j,
        "is_cryptoswap": is_cryptoswap,
        "is_underlying_swap": is_underlying_swap,
        "is_wrapper": is_wrapper,
    }
