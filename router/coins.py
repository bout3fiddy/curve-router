from router.common import BasePool, Coin, Wrapper

# ----- Coins ----- #

USDT = Coin(
    "0xdAC17F958D2ee523a2206206994597C13D831ec7".lower(),
    network="Mainnet",
    decimals=6,
)
USDC = Coin(
    "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower(),
    network="Mainnet",
    decimals=18,
)
DAI = Coin(
    "0x6B175474E89094C44Da98b954EedeAC495271d0F".lower(),
    network="Mainnet",
    decimals=18,
)
FEI = Coin(
    address="0x956F47F50A910163D8BF957Cf5846D573E7f87CA".lower(),
    network="Mainnet",
    decimals=18,
)
cvxCRV = Coin(
    "0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7".lower(),
    network="Mainnet",
    decimals=18,
)
CRV = Coin(
    "0xD533a949740bb3306d119CC777fa900bA034cd52".lower(),
    network="Mainnet",
    decimals=18,
)

WETH = Coin(
    address="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
    network="Mainnet",
    decimals=18,
)
ETH = Coin(
    address="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE".lower(),
    network="Mainnet",
    decimals=18,
)


# ----- WETH ----- #


WETH_ETH_POOL = Wrapper(
    pool="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
    network="Mainnet",
    coin_a=WETH.address,
    coin_a_decimals=WETH.decimals,
    coin_b=ETH.address,
    coin_b_decimals=ETH.decimals,
    is_cryptoswap=False,
    is_stableswap=False,
    is_metapool=False,
    base_pool="0x0",
    is_underlying_swap=False,
    i=0,
    j=0,
    wrap=False,
)
ETH_WETH_POOL = Wrapper(
    pool="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
    network="Mainnet",
    coin_a=ETH.address,
    coin_a_decimals=ETH.decimals,
    coin_b=WETH.address,
    coin_b_decimals=WETH.decimals,
    is_cryptoswap=False,
    is_stableswap=False,
    is_metapool=False,
    base_pool="0x0",
    is_underlying_swap=False,
    i=0,
    j=0,
    wrap=True,
)

# ----- BasePools ----- #

THREECRV_TOKEN = Coin(
    "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490",
    network="Mainnet",
    decimals=18,
    is_lp_token=True
)

THREECRV_BASEPOOL = BasePool(
    pool_address="0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7".lower(),
    lp_token=THREECRV_TOKEN,
    network="Mainnet",
    lp_token_decimals=18,
    coins=[DAI, USDC, USDT],  # this is also how coin indices are arranged
)
