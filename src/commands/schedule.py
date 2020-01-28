from src.datasource.jra import io as jra

def get(year, is_place):
    """Getting the schedule on JRA with argument's year
    """
    return jra.get_race_name_list(year, is_place)