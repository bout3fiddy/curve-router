from router.common import BasePool

# ---- Mainnet ----
THREECRV_TOKEN_MAINNET = "0x6c3f90f043a72fa612cbac8115ee7e52bde6e490".lower()
USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7".lower()
USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower()
DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F".lower()
THREECRV_BASEPOOL_MAINNET = BasePool(
    pool_address="0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7".lower(),
    lp_token=THREECRV_TOKEN_MAINNET,
    network="Mainnet",
    lp_token_decimals=18,
    coins=[DAI, USDC, USDT],  # this is also how coin indices are arranged
)

crvrenBTC_wBTC_sBTC_TOKEN = (
    "0x075b1bb99792c9E1041bA13afEf80C91a1e70fB3".lower()
)
renbBTC = "0xEB4C2781e4ebA804CE9a9803C67d0893436bB27D".lower()
wBTC = "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599".lower()
sBTC = "0xfE18be6b3Bd88A2D2A7f928d00292E7a9963CfC6".lower()
THREEBTC_BASEPOOL_MAINNET = BasePool(
    pool_address="0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714".lower(),
    lp_token=crvrenBTC_wBTC_sBTC_TOKEN,
    network="Mainnet",
    lp_token_decimals=18,
    coins=[renbBTC, wBTC, sBTC],  # this is also how coin indices are arranged
)

crvrenBTC_wBTC_TOKEN = "0x49849C98ae39Fff122806C06791Fa73784FB3675".lower()
TWOBTC_BASEPOOL_MAINNET = BasePool(
    pool_address="0x93054188d876f558f4a66B2EF1d97d16eDf0895B".lower(),
    lp_token=crvrenBTC_wBTC_TOKEN,
    network="Mainnet",
    lp_token_decimals=18,
    coins=[renbBTC, wBTC],  # this is also how coin indices are arranged
)

# ---- Arbitrum ----
TWOCRV_TOKEN_ARBITRUM = "0x7f90122BF0700F9E7e1F688fe926940E8839F353".lower()
USDT_ARB = "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9".lower()
USDC_ARB = "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8".lower()
TWOCRV_BASEPOOL_ARBITRUM = BasePool(
    pool_address=TWOCRV_TOKEN_ARBITRUM,
    lp_token=TWOCRV_TOKEN_ARBITRUM,
    network="Arbitrum",
    lp_token_decimals=18,
    coins=[USDC_ARB, USDT_ARB],  # this is also how coin indices are arranged
)

TWOBTC_TOKEN_ARBITRUM = "0x3E01dD8a5E1fb3481F0F589056b428Fc308AF0Fb".lower()
wBTC_ARB = "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f".lower()
renBTC_ARB = "0xDBf31dF14B66535aF65AaC99C32e9eA844e14501".lower()
TWOBTC_BASEPOOL_ARBITRUM = BasePool(
    pool_address=TWOBTC_TOKEN_ARBITRUM,
    lp_token=TWOBTC_TOKEN_ARBITRUM,
    network="Arbitrum",
    lp_token_decimals=18,
    coins=[wBTC_ARB, renBTC_ARB],  # this is also how coin indices are arranged
)

# ---- Optimism ----
THREECRV_TOKEN_OPTIMISM = "0x1337BedC9D22ecbe766dF105c9623922A27963EC".lower()
DAI_OPTIMISM = "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1".lower()
USDC_OPTIMISM = "0x7F5c764cBc14f9669B88837ca1490cCa17c31607".lower()
USDT_OPTIMISM = "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58".lower()
THREECRV_BASEPOOL_OPTIMISM = BasePool(
    pool_address=THREECRV_TOKEN_OPTIMISM,
    lp_token=THREECRV_TOKEN_OPTIMISM,
    network="Optimism",
    lp_token_decimals=18,
    coins=[DAI_OPTIMISM, USDC_OPTIMISM, USDT_OPTIMISM],
)

# ---- Fantom ----
G3CRV_TOKEN = "0xD02a30d33153877BC20e5721ee53DeDEE0422B2F".lower()

# MultiChain bridged versions of 3CRV stables
DAI_FANTOM = "0x8D11eC38a3EB5E956B052f67Da8Bdc9bef8Abf3E".lower()
USDC_FANTOM = "0x04068DA6C83AFCFA0e13ba15A6696662335D5B75".lower()
fUSDT_FANTOM = "0x049d68029688eAbF473097a2fC38ef61633A3C7A".lower()

# gTOKENS
gDAI_FANTOM = "0x07E6332dD090D287d3489245038daF987955DCFB".lower()
gUSDC_FANTOM = "0xe578C856933D8e1082740bf7661e379Aa2A30b26".lower()
gfUSDT_FANTOM = "0x940F41F0ec9ba1A34CF001cc03347ac092F5F6B5".lower()

G3CRV_BASEPOOL_FANTOM = BasePool(
    pool_address="0x0fa949783947Bf6c1b171DB13AEACBB488845B3f".lower(),
    lp_token=G3CRV_TOKEN,
    network="Fantom",
    lp_token_decimals=18,
    coins=[DAI_FANTOM, USDC_FANTOM, fUSDT_FANTOM],
)
G3CRV_BASEPOOL_FANTOM_gTOKENS = BasePool(
    pool_address="0x0fa949783947Bf6c1b171DB13AEACBB488845B3f".lower(),
    lp_token=G3CRV_TOKEN,
    network="Fantom",
    lp_token_decimals=18,
    coins=[gDAI_FANTOM, gUSDC_FANTOM, gfUSDT_FANTOM],
    is_lending=True,
)

TWOCRV_TOKEN_FANTOM = "0x27E611FD27b276ACbd5Ffd632E5eAEBEC9761E40".lower()
TWOCRV_BASEPOOL_FANTOM = BasePool(
    pool_address=TWOCRV_TOKEN_FANTOM,
    lp_token=TWOCRV_TOKEN_FANTOM,
    network="Fantom",
    lp_token_decimals=18,
    coins=[DAI_FANTOM, USDC_FANTOM],
)

BTCCRV_FANTOM_LP_TOKEN = "0x5B5CFE992AdAC0C9D48E05854B2d91C73a003858".lower()
MULTICHAIN_WBTC_FANTOM = "0x321162Cd933E2Be498Cd2267a90534A804051b11".lower()
renBTC_FANTOM = "0xDBf31dF14B66535aF65AaC99C32e9eA844e14501".lower()
TWOBTC_BASEPOOL_FANTOM = BasePool(
    pool_address="0x3eF6A01A0f81D6046290f3e2A8c5b843e738E604".lower(),
    lp_token=BTCCRV_FANTOM_LP_TOKEN,
    network="Fantom",
    lp_token_decimals=18,
    coins=[MULTICHAIN_WBTC_FANTOM, renBTC_FANTOM],
)

# ---- Matic/Polygon ----
am3CRV_TOKEN = "0xD02a30d33153877BC20e5721ee53DeDEE0422B2F".lower()

# Bridged versions of 3CRV stables
DAI_MATIC = "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063".lower()
USDC_MATIC = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174".lower()
USDT_MATIC = "0xc2132D05D31c914a87C6611C10748AEb04B58e8F".lower()

# gTOKENS
amDAI_MATIC = "0x27F8D03b3a2196956ED754baDc28D73be8830A6e".lower()
amUSDC_MATIC = "0x1a13F4Ca1d028320A707D99520AbFefca3998b7F".lower()
amUSDT_MATIC = "0x60D55F02A771d515e077c9C2403a1ef324885CeC".lower()

am3CRV_BASEPOOL_MATIC = BasePool(
    pool_address="0x445FE580eF8d70FF569aB36e80c647af338db351".lower(),
    lp_token=am3CRV_TOKEN,
    network="Matic",
    lp_token_decimals=18,
    coins=[DAI_MATIC, USDC_MATIC, USDT_MATIC],
)
am3CRV_BASEPOOL_MATIC_amTOKENS = BasePool(
    pool_address="0x445FE580eF8d70FF569aB36e80c647af338db351".lower(),
    lp_token=am3CRV_TOKEN,
    network="Matic",
    lp_token_decimals=18,
    coins=[amDAI_MATIC, amUSDC_MATIC, amUSDT_MATIC],
    is_lending=True,
)

BTCCRV_MATIC_LP_TOKEN = "0xf8a57c1d3b9629b77b6726a042ca48990a84fb49".lower()
WBTC_MATIC = "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6".lower()
amWBTC_MATIC = "0x5c2ed810328349100A66B82b78a1791B101C9D61".lower()
renBTC_MATIC = "0xDBf31dF14B66535aF65AaC99C32e9eA844e14501".lower()

TWOBTC_BASEPOOL_MATIC = BasePool(
    pool_address="0xC2d95EEF97Ec6C17551d45e77B590dc1F9117C67".lower(),
    lp_token=BTCCRV_MATIC_LP_TOKEN,
    network="Fantom",
    lp_token_decimals=18,
    coins=[WBTC_MATIC, renBTC_MATIC],
)

TWOBTC_BASEPOOL_MATIC_LENDING = BasePool(
    pool_address="0xC2d95EEF97Ec6C17551d45e77B590dc1F9117C67".lower(),
    lp_token=BTCCRV_MATIC_LP_TOKEN,
    network="MATIC",
    lp_token_decimals=18,
    coins=[amWBTC_MATIC, renBTC_MATIC],
    is_lending=True,
)

# ---- Avalanche ----


# ---- xDAI/Gnosis ----


# ---- BasePools ----
BASE_POOLS = {
    "Mainnet": [
        THREECRV_BASEPOOL_MAINNET,
        THREEBTC_BASEPOOL_MAINNET,
        TWOBTC_BASEPOOL_MAINNET,
    ],
    "Arbitrum": [TWOCRV_BASEPOOL_ARBITRUM, TWOBTC_BASEPOOL_ARBITRUM],
    "Optimism": [THREECRV_BASEPOOL_OPTIMISM],
    "Fantom": [
        G3CRV_BASEPOOL_FANTOM,
        G3CRV_BASEPOOL_FANTOM_gTOKENS,
        TWOCRV_BASEPOOL_FANTOM,
        TWOBTC_BASEPOOL_FANTOM,
    ],
    "Matic": [
        am3CRV_BASEPOOL_MATIC,
        am3CRV_BASEPOOL_MATIC_amTOKENS,
        TWOBTC_BASEPOOL_MATIC,
        TWOBTC_BASEPOOL_MATIC_LENDING,
    ],
    "Avalanche": [],
    "xDAI": [],
}
