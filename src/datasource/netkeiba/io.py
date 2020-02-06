import re
import requests
import urllib.parse
import pandas as pd
from datetime import datetime
from collections import namedtuple
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


##############################################################################
# Define constants
##############################################################################
# Max retyr count
MAX_RETRY_COUNT = 3
# Datasource URL
BASE_URL = "https://db.netkeiba.com"
# Use for getting race result
RACE_RESULT_HEADER = ["date", "place", "weather", "race_index", "race_name", "movie", "distance", "horses", "cource_situation", "winning_time", "pace", "winning_horse", "jockey", "trainer", "second_horse", "third_horse"]
RACE_RESULT_REMOVE_HEADER = ["race_index", "movie", "winning_time", "pace", "winning_horse", "jockey", "trainer", "second_horse", "third_horse"]
# Use for getting race details
RACE_DETAILS_HEADER = ["arrival_order", "frame_number", "horse_number", "horse_name", "horse_sex_age", "loaf_weight", "jockey_name", "time", "arrival_difference", "odds", "favorite", "horse_weight", "trainer_name"]
# Use for getting horse details
HORSE_DETAILS_HEADER_10_ITEMS = ["birthday", "trainer", "owner", "producer", "origin", "trading_price", "winnings", "results", "main_race", "close_relatives"]
HORSE_DETAILS_HEADER_11_ITEMS = ["birthday", "trainer", "owner", "one_bite", "producer", "origin", "trading_price", "winnings", "results", "main_race", "close_relatives"]
# Define the returning DataFrame header
JOINED_RESULT_DETAILS_HEADER = ["year", "date", "place", "weather", "race_name", "grade", "distance", "horses", "cource_situation", "arrival_order", "frame_number", "horse_number", "horse_name", "horse_sex", "horse_age", "loaf_weight", "jockey_name", "time", "arrival_difference", "odds", "favorite", "horse_weight", "horse_changed_weight", "trainer_name", "race_details_url", "horse_details_url", "jockey_details_url", "trainer_details_url"]
# Returning DataFrame column types
JOINED_RESULT_DETAILS_TYPES = {"year": "int", "date": "str", "place": "str", "weather": "str", "race_name": "str", "distance": "str", "horses": "str", "cource_situation": "str", "arrival_order": "str", "frame_number": "str", "horse_number": "str", "horse_name": "str", "horse_sex": "str", "horse_age": "int", "loaf_weight": "str", "jockey_name": "str", "time": "str", "arrival_difference": "str", "odds": "str", "favorite": "str", "horse_weight": "integer", "horse_changed_weight": "int", "trainer_name": "str", "race_details_url": "str", "horse_details_url": "str", "jockey_details_url": "str", "trainer_details_url": "str"}
# NamedTuple for URL parameters
URL_PARAMS = namedtuple("URL_PARAMS", ("PID", "WORD", "TRACK", "START_YEAR", "START_MONTH", "END_YEAR", "END_MONTH", "PAGE", "SORT_KEY", "SORT_TYPE", "LIST"))
url_params = URL_PARAMS(
    PID = "pid",
    WORD = "word",
    TRACK = "track[]",
    START_YEAR = "start_year",
    START_MONTH = "start_mon",
    END_YEAR = "end_year",
    END_MONTH = "end_mon",
    PAGE = "page",
    SORT_KEY = "sort_key",
    SORT_TYPE = "sort_type",
    LIST = "list"
)
PID_LIST = namedtuple("PID_LIST", ("RACE", "RACE_LIST", "JOCKEY", "JOCKEY_LIST", "HORSE", "HORSE_LIST", "TRAINER", "TRAINER_LIST"))
pid_list = PID_LIST(
    RACE = "race",
    RACE_LIST = "race_list",
    JOCKEY = "jockey",
    JOCKEY_LIST = "jockey_list",
    HORSE = "horse",
    HORSE_LIST = "horse_list",
    TRAINER = "trainer",
    TRAINER_LIST = "trainer_list"
)
TRACK_LIST = namedtuple("TRACK_LIST", ("TURF", "DIRT", "HURDLE"))
track_list = TRACK_LIST(
    TURF = "1",
    DIRT = "2",
    HURDLE = "3"
)

##############################################################################
# Functions for corresponding to retry
##############################################################################
def requests_retry_session(
    backoff_factor=0.3, status_forcelist=(500, 502, 504)
):
    session = requests.Session()
    retry = Retry(
        total=MAX_RETRY_COUNT,
        read=MAX_RETRY_COUNT,
        connect=MAX_RETRY_COUNT,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

##############################################################################
# Functions for getting the history data
##############################################################################
def get_race_result(params):
    # Create URL parameters for getting horse racing results
    params_track = None
    params = {key: params[key] for key in params if params[key]}
    params[url_params.PID] = pid_list.RACE_LIST
    params[url_params.LIST] = 100
    if url_params.WORD in params.keys():
        params[url_params.WORD] = str(
            params[url_params.WORD].encode("EUC-JP")
        )[2:-1].replace("\\x", "%")
    # Convert array parameters to be able to use URL parameters
    if url_params.TRACK in params.keys():
        params_track = "&".join([
            eval("track_list." + val)
            for val in params[url_params.TRACK]
        ])
        del params[url_params.TRACK]
    req_url = BASE_URL + "/?" + urllib.parse.urlencode(params)
    if params_track:
        req_url += "&" + params_track
    # Get the response by using the converted URL
    r = requests_retry_session().get(req_url)
    soup = BeautifulSoup(r.text.encode(r.encoding), "lxml")
    r.connection.close()
    parsed_table = soup.find_all("table")[0]
    df = pd.read_html(str(parsed_table))[0]
    if not (len(RACE_RESULT_HEADER) == len(df.columns)):
        return None
    df.columns = RACE_RESULT_HEADER
    # Remove needless charactor in the [place] column
    df["place"] = df["place"].replace("[0-9]", "", regex=True)
    # Adding the url of race_name
    df["race_details_url"] = [
        "".join([
            BASE_URL + link.get("href")
            for link in tag.find_all("a") 
            if re.match("\/race\/[0-9]+", link.get("href"))
        ])
        for tag in parsed_table.find_all("tr")
    ][1:]
    # Separate the complex data columns
    df["grade"] = df["race_name"].apply(
        lambda x: re.search(r"G[1-3]", x).group().replace("G", "")
        if re.search(r"G[1-3]", x) else None
    )
    df["race_name"] = df["race_name"].replace(
        "[(]G[1-3][)]|[(]OP[)]", "", regex=True
    )
    cource_kind_dict = {"芝": "turf", "ダ": "dirt", "障": "hurdle"}
    df["race_category"] = df["distance"].apply(
        lambda x: cource_kind_dict[x[:1]]
        if not x[:1].isdecimal() else None
    )
    df["distance"] = df["distance"].apply(
        lambda x: x[1:] if not x[:1].isdecimal() else x
    )
    # Convert type of date column
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
    df["year"] = df["date"].apply(lambda x: x.year)
    # Return the DataFrame
    return df
        
def get_race_details(details_url):
    r = requests_retry_session().get(details_url)
    soup = BeautifulSoup(r.text.encode(r.encoding), "lxml")
    r.connection.close()
    parsed_table = soup.find_all("table")[0]
    df = pd.read_html(str(parsed_table))[0]
    if len(RACE_DETAILS_HEADER) == len(df.columns):
        df.columns = RACE_DETAILS_HEADER
        # Separate the complex data columns
        df["horse_changed_weight"] = df["horse_weight"].apply(
            lambda x: int(
                re.search(r"[(][+-]*[0-9]*[)]", x).group().replace(
                    "(", ""
                ).replace(")", "") 
                if re.search(r"[(][+-]*[0-9]*[)]", x) else 0
                or 0
            )
        )
        df["horse_weight"] = df["horse_weight"].replace(
            "[(][+-]*[0-9]*[)]", "", regex=True
        )
        df["horse_sex"] = df["horse_sex_age"].fillna("").str[0]
        df["horse_age"] = df["horse_sex_age"].fillna("").str[1:]
        # Adding the url of details pages
        df["race_details_url"] = details_url
        df["horse_details_url"] = [
            "".join([
                BASE_URL + link.get("href")
                for link in tag.find_all("a") 
                if re.match("\/horse\/[0-9]+", link.get("href"))
            ])
            for tag in parsed_table.find_all("tr")
        ][1:]
        df["jockey_details_url"] = [
            "".join([
                BASE_URL + link.get("href")
                for link in tag.find_all("a") 
                if re.match("\/jockey\/[0-9]+", link.get("href"))
            ])
            for tag in parsed_table.find_all("tr")
        ][1:]
        df["trainer_details_url"] = [
            "".join([
                BASE_URL + link.get("href")
                for link in tag.find_all("a") 
                if re.match("\/trainer\/[0-9]+", link.get("href"))
            ])
            for tag in parsed_table.find_all("tr")
        ][1:]
    return df

