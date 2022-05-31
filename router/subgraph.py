import requests


def get_pool_data(api: str):

    # todo: when there are more than 1000 pools, this will need to be updated
    query = """
    {
        platforms {
            pools(first: 1000) {
                coins
                coinDecimals
                address
                isV2
                metapool
                basePool
                dailyPoolSnapshots(
                    first: 1,
                    orderBy: timestamp,
                    orderDirection: desc
                ) {
                    reserves
                    reservesUsd
                }
            }
        }
    }
    """
    r = requests.post(api, json={"query": query})
    data = dict(r.json())
    pool_data = data["data"]["platforms"][0]["pools"]

    # de-nest pool data to include pool reserves
    de_nested_pool_data = []
    for _pool_data in pool_data:
        latest_pool_snapshot = _pool_data["dailyPoolSnapshots"][0]
        de_nested_pool_data.append(
            {
                "coins": _pool_data["coins"],
                "coinDecimals": _pool_data["coinDecimals"],
                "address": _pool_data["address"],
                "isV2": _pool_data["isV2"],
                "metapool": _pool_data["metapool"],
                "basePool": _pool_data["basePool"],
                "reserves": [
                    float(i) for i in latest_pool_snapshot["reserves"]
                ],
                "reservesUsd": [
                    float(i) for i in latest_pool_snapshot["reservesUsd"]
                ],
            }
        )

    return de_nested_pool_data
