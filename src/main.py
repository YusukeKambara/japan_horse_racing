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
    Track name to get the race result
    Can be selected multiple values
    """
)
@click.option(
    "--place", "-p", multiple=True,
    type=click.Choice(list(netkeiba.place_list._asdict().keys())),
    help="""
    Place name to get the race result
    Can be selected multiple values
    """
)
@click.option(
    "--start_year", "-sy", type=int, default=datetime.now().year,
    help="Year to start to get the race result"
)
@click.option(
    "--start_month", "-sm", type=int,
    help="Month to start to get the race result"
)
@click.option(
    "--end_year", "-ey", type=int,
    help="Year to end to get the race result"
)
@click.option(
    "--end_month", "-em", type=int,
    help="Month to end to get the race result"
)
def get_result(
    name, track, place, start_year, start_month, end_year, end_month
):
    """Getting the race result of JRA horse racing
    """
    params = {
        netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
        netkeiba.url_params.WORD: name,
        netkeiba.url_params.TRACK: track,
        netkeiba.url_params.PLACE: place,
        netkeiba.url_params.START_YEAR: start_year,
        netkeiba.url_params.START_MONTH: start_month,
        netkeiba.url_params.END_YEAR: end_year,
        netkeiba.url_params.END_MONTH: end_month
    }
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