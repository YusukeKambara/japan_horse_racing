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
    if df is None or df.empty:
        return None
    return pd.merge(
        df,
        pd.concat(
            [
                netkeiba.get_race_details(url)
                for url in df["race_details_url"].to_list()
            ],
            ignore_index=True,
            sort=False
        ),
        how="left"
    )[netkeiba.JOINED_RESULT_DETAILS_HEADER]