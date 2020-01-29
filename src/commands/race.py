import pandas as pd
from datasource.netkeiba import io as netkeiba

def get_result(params):
    """Getting the race data on JRA with argument's params
    """
    return netkeiba.get_race_result(params)

def get_details(params):
    """Getting the race details on JRA with argument's params
    """
    df = netkeiba.get_race_result(params)
    return pd.concat(
        [
            netkeiba.get_race_details(url)
            for url in df["race_details_url"].to_list()
        ],
        ignore_index=True
    )