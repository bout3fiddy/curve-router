import pytest
from brownie import ZERO_ADDRESS, Swaps, accounts

from router.constants import ADDRESS_PROVIDER
from router.curve_router import initialise


@pytest.fixture(scope="module")
def alice():
    return accounts[0]


@pytest.fixture(scope="module")
def registry_swap(alice):
    return Swaps.deploy(ADDRESS_PROVIDER, ZERO_ADDRESS, {"from": alice})


@pytest.fixture(scope="module")
def router_mainnet():
    return initialise("Mainnet")


@pytest.fixture(scope="module")
def router_arbitrum():
    return initialise("Arbitrum")


@pytest.fixture(scope="module")
def router_optimism():
    return initialise("Optimism")


@pytest.fixture(scope="module")
def router_avalanche():
    return initialise("Avalanche")


@pytest.fixture(scope="module")
def router_matic():
    return initialise("Matic")


@pytest.fixture(scope="module")
def router_xdai():
    return initialise("xDAI")
