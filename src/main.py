import io
import os
import click
from datetime import datetime
from commands import schedule as commands_schedule

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

if __name__ == "__main__":
    main()