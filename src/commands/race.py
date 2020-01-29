from datasource.netkeiba import io as netkeiba

def get_result(params):
    """Getting the race data on JRA with argument's params
    """
    return netkeiba.get_race_result(params)