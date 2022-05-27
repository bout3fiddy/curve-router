import pytest
from brownie import ZERO_ADDRESS, CurveRouter, accounts


@pytest.fixture(scope="session")
def alice():
    return accounts[0]


@pytest.fixture(scope="session")
def curve_router(alice):
    return CurveRouter.deploy({"from": alice})


@pytest.fixture(scope="session")
def route_one_hop():
    pool_addresses = [ZERO_ADDRESS] * 10
    pool_addresses[0] = "0x01fe650ef2f8e2982295489ae6adc1413bf6011f"
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


@pytest.fixture(scope="session")
def route_rai_ageur():
    pool_addresses = [
        "0x618788357d0ebd8a37e763adab3bc575d54c2c7d",
        "0xceaf7747579696a2f0bb206a14210e3c9e6fb269",
        "0x4e0915c88bc70750d68c481540f081fefaf22273",
        "0x98a7f18d4e56cfe84e3d081b40001b3d5bd3eb8b",
        "0xb9446c4ef5ebe66268da6700d26f96273de3d571",
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        ZERO_ADDRESS,
        ZERO_ADDRESS,
    ]
    i = [0, 1, 2, 0, 2, 0, 0, 0, 0, 0]
    j = [1, 0, 0, 1, 0, 0, 0, 0, 0, 0]
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
