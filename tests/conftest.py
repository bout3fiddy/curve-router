import pytest
from brownie import Swaps, ZERO_ADDRESS, accounts

from router.constants import ADDRESS_PROVIDER
from router.curve_router import initialise


@pytest.fixture(scope="session")
def alice():
    return accounts[0]


@pytest.fixture(scope="session")
def registry_swap(alice):
    return Swaps.deploy(ADDRESS_PROVIDER, ZERO_ADDRESS, {"from": alice})


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
