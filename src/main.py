import io
import os
import click
import pandas as pd
from datetime import datetime
from commands import schedule as commands_schedule
from commands import race as commands_race
from datasource.netkeiba import io as netkeiba


pd.set_option("display.max_columns", None)

def main():
    cmd()

@click.group()
def cmd():
    """First layer sub-command group
    """
    pass

@cmd.group()
def schedule():
    """Second layer sub-command group
    """
    pass

@cmd.group()
def race():
    """Second layer sub-command group
    """
    pass

@schedule.command()
@click.option(
    "--year", "-y", type=int, default=datetime.now().year,
    help="Target year to get the schedule"
)
@click.option(
    "--place", "-p", is_flag=True,
    help="""
        Getting place data or not.
        If you cannot set this flag, you get only place.
    """
)
def get(year, place):
    """Getting the schedule of JRA horse racing
    """
    name_list = commands_schedule.get(year, place)
    print(name_list)
    return name_list

@race.command()
@click.option(
    "--name", "-n", type=str,
    help="Race name to get the race result"
)
@click.option(
    "--track", "-t", multiple=True,
    type=click.Choice(list(netkeiba.track_list._asdict().keys())),
    help="""
    [multiple] Track name to get the race result
    """
)
@click.option(
    "--place", "-p", multiple=True,
    type=click.Choice(list(netkeiba.place_list._asdict().keys())),
    help="""
    [multiple] Place name to get the race result
    """
)
@click.option(
    "--course-situation", "-cs", multiple=True,
    type=click.Choice(list(netkeiba.course_situation_list._asdict().keys())),
    help="""
    [multiple] Course situation to get the race result
    """
)
@click.option(
    "--race-conditions", "-rs", multiple=True,
    type=click.Choice(list(netkeiba.race_conditions_list._asdict().keys())),
    help="""
    [multiple] Race conditions to get the race result
    """
)
@click.option(
    "--horse-age", "-ha", multiple=True,
    type=click.Choice(list(netkeiba.horse_age_list._asdict().keys())),
    help="""
    [multiple] Horse age to get the race result
    """
)
@click.option(
    "--grade", "-g", multiple=True,
    type=click.Choice(list(netkeiba.grade_list._asdict().keys())),
    help="""
    [multiple] Grade to get the race result
    """
)
@click.option(
    "--distance-from", "-df", type=int,
    help="Minimum distance to get the race result"
)
@click.option(
    "--distance-to", "-dt", type=int,
    help="Maximum distance to get the race result"
)
@click.option(
    "--start-year", "-sy", type=int, default=datetime.now().year,
    help="Year to start to get the race result"
)
@click.option(
    "--start-month", "-sm", type=int,
    help="Month to start to get the race result"
)
@click.option(
    "--end-year", "-ey", type=int,
    help="Year to end to get the race result"
)
@click.option(
    "--end-month", "-em", type=int,
    help="Month to end to get the race result"
)
def get_result(
    name, track, place, course_situation, race_conditions, horse_age,
    grade, distance_from, distance_to,
    start_year, start_month, end_year, end_month
):
    """Getting the race result of JRA horse racing
    """
    params = {
        netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
        netkeiba.url_params.WORD: name,
        netkeiba.url_params.TRACK: [
            eval("netkeiba.track_list." + val) for val in track
        ],
        netkeiba.url_params.PLACE: [
            eval("netkeiba.place_list." + val) for val in place
        ],
        netkeiba.url_params.COURSE_SITUATION: [
            eval("netkeiba.course_situation_list." + val)
            for val in course_situation
        ],
        netkeiba.url_params.RACE_CONDITIONS: [
            eval("netkeiba.race_conditions_list." + val)
            for val in race_conditions
        ],
        netkeiba.url_params.HORSE_AGE: [
            eval("netkeiba.horse_age_list." + val) for val in horse_age
        ],
        netkeiba.url_params.GRADE: [
            eval("netkeiba.grade_list." + val) for val in grade
        ],
        netkeiba.url_params.DISTANCE_FROM: distance_from,
        netkeiba.url_params.DISTANCE_TO: distance_to,
        netkeiba.url_params.START_YEAR: start_year,
        netkeiba.url_params.START_MONTH: start_month,
        netkeiba.url_params.END_YEAR: end_year,
        netkeiba.url_params.END_MONTH: end_month
    }
    print(params)
    results = commands_race.get_result(params)
    print(results)
    return results

@race.command()
@click.option(
    "--name", "-n", type=str,
    help="Target name to get the race details"
)
@click.option(
    "--year", "-y", type=int, default=datetime.now().year,
    help="Target year to get the race details"
)
@click.option(
    "--month", "-m", type=int, default=datetime.now().month,
    help="Target month to get the race details"
)
def get_details(name, year, month):
    """Getting the race details of JRA horse racing
    """
    params = {
        netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
        netkeiba.url_params.WORD: name,
        netkeiba.url_params.START_YEAR: year,
        netkeiba.url_params.END_YEAR: year,
        netkeiba.url_params.START_MONTH: month,
        netkeiba.url_params.END_MONTH: month
    }
    details = commands_race.get_details(params)
    print(details)
    return details

if __name__ == "__main__":
    main()