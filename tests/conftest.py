import pytest
from brownie import Swaps, accounts

from router.curve_router import initialise


@pytest.fixture(scope="session")
def alice():
    return accounts[0]


@pytest.fixture(scope="session")
def curve_router(alice):
    return Swaps.deploy({"from": alice})


@pytest.fixture(scope="session")
def router_mainnet():
    return initialise("Mainnet")


@pytest.fixture(scope="session")
def router_arbitrum():
    return initialise("Arbitrum")


@pytest.fixture(scope="session")
def router_optimism():
    return initialise("Optimism")


@pytest.fixture(scope="session")
def router_avalanche():
    return initialise("Avalanche")


@pytest.fixture(scope="session")
def router_matic():
    return initialise("Matic")


@pytest.fixture(scope="session")
def router_xdai():
    return initialise("xDAI")
