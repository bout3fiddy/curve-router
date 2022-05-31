from router.common import Wrapper
from router.constants import ETH, WETH

WETH_ETH_POOL = Wrapper(
    pool="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
    network="Mainnet",
    coin_a=WETH,
    coin_b=ETH,
    is_cryptoswap=False,
    is_stableswap=False,
    is_metapool=False,
    base_pool="0x0",
    is_underlying_swap=False,
    i=0,
    j=0,
    wrap=False,
    pool_tvl_usd=0,  # this tvl doesn't count
)
ETH_WETH_POOL = Wrapper(
    pool="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower(),
    network="Mainnet",
    coin_a=ETH,
    coin_b=WETH,
    is_cryptoswap=False,
    is_stableswap=False,
    is_metapool=False,
    base_pool="0x0",
    is_underlying_swap=False,
    i=0,
    j=0,
    wrap=True,
    pool_tvl_usd=0,  # this tvl doesn't count
)
