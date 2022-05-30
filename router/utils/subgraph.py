import datetime

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
            }
        }
    }
    """
    r = requests.post(api, json={"query": query})
    data = dict(r.json())
    pool_data = data["data"]["platforms"][0]["pools"]

    return pool_data


def get_num_swaps_pool(pool_addr, api, activity_duration: int = 365):

    time_end = int(datetime.datetime.now().timestamp())
    time_start = int(
        datetime.datetime.now().timestamp() - 24 * 3600 * activity_duration
    )

    query = f"""
    {{
      swapEvents(
        first: 1000,
        where: {{
          pool: "{pool_addr.lower()}"
          timestamp_gte: {time_start}
          timestamp_lt: {time_end}
        }}
      ) {{
        timestamp
        block
      }}
    }}
    """
    r = requests.post(api, json={"query": query})
    queried_data = dict(r.json())
    if "data" not in queried_data:
        print("no data")
        return 0
    swap_events = queried_data["data"]["swapEvents"]
    return len(swap_events)


def get_latest_pool_coin_reserves(pool_addr, api):

    query = f"""
    {{
      dailyPoolSnapshots(
        first: 1,
        orderBy: timestamp,
        orderDirection: desc,
        where:{{
          pool: "{pool_addr.lower()}"
        }}
      ) {{
        reserves
      }}
    }}
    """
    r = requests.post(api, json={"query": query})
    queried_data = dict(r.json())["data"]["dailyPoolSnapshots"][0]["reserves"]
    return [int(i) for i in queried_data]
