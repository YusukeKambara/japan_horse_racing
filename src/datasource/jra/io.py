import io
import requests
import zipfile
from datetime import datetime
from icalendar import Calendar


##############################################################################
# Define constants
##############################################################################
# Use for getting race name list
ICAL_FILE_DOWNLOAD_URL = "http://www.jra.go.jp/keiba/common/calendar/jrarace{year}.zip"
ICAL_FILE_NAME = "jrarace{year}.ics"
ICAL_PLACE_DOWNLOAD_URL = "http://www.jra.go.jp/keiba/common/calendar/jrakaisai{year}.zip"
ICAL_PLACE_NAME = "jrakaisai{year}.ics"

##############################################################################
# DataIO functions
##############################################################################
def get_race_name_list(target_year, is_place):
    """Getting the race name and event date 
    
    Arguments:
        target_year {int} -- target year to get the data
        is_place {bool} -- [description]
    
    Returns:
        [list in dict] -- event date and race name
    """
    zip_url = ICAL_PLACE_DOWNLOAD_URL if is_place else ICAL_FILE_DOWNLOAD_URL
    ical_name = ICAL_PLACE_NAME if is_place else ICAL_FILE_NAME
    url_path = zip_url.format(year=target_year)
    file_name = ical_name.format(year=target_year)
    zip_obj = requests.get(url_path)
    with zipfile.ZipFile(io.BytesIO(zip_obj.content)) as unzipped_obj:
        with unzipped_obj.open(file_name) as ical_obj:
            cal = Calendar.from_ical(ical_obj.read())
            return [
                {
                    "date": ev["dtend"].dt,
                    "title": str(ev["summary"]).split("(")[0]
                }
                for ev in cal.walk()
                if ev.name == "VEVENT"
            ]
