import unittest
import requests
import pandas as pd
from src.datasource.netkeiba import io as netkeiba

class TestIo(unittest.TestCase):
    """Test class for testing the netkeiba datasource
    
    Arguments:
        unittest {[type]} -- [description]
    """

    @classmethod
    def setUpClass(cls):
        print("*" * 80 + "\nStart to test [datasource.netkeiba] module\n" + "*" * 80)

    def test_requests_retry_session(self):
        """Testing to get the session object
        """
        session = netkeiba.requests_retry_session()
        assert type(session) == requests.Session

    def test_get_race_result_with_race_name_param(self):
        """Testing to get the DataFrame with word parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.WORD: "有馬記念"
        }
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert all(["有馬記念" in name for name in df["race_name"].to_list()])

    def test_get_race_result_with_track_param(self):
        """Testing to get the DataFrame with track parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.START_YEAR: 2019,
            netkeiba.url_params.TRACK: ["DIRT"]
        }
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert all(["dirt" in name for name in df["race_category"].to_list()])

    def test_get_race_result_with_place_param(self):
        """Testing to get the DataFrame with place parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.START_YEAR: 2019,
            netkeiba.url_params.PLACE: ["KYOTO"]
        }
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert all(["京都" in name for name in df["place"].to_list()])

    def test_get_race_result_with_course_situation_param(self):
        """Testing to get the DataFrame with course situation parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.START_YEAR: 2019,
            netkeiba.url_params.TRACK: ["DIRT"],
            netkeiba.url_params.COURSE_SITUATION: ["HEAVY_HOLDING"]
        }
        # [TODO]
        # In case of track is hurdle, possibility we get the SOFT_YIELDING data,
        # even if we set the search condition to HEAVY_HOLDING.
        # So, I check only dirt data.
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert all(["不" in name for name in df["course_situation"].to_list()])

    def test_get_race_result_with_race_conditions_param(self):
        """Testing to get the DataFrame with race conditions parameters
        """
        # [TODO]
        # In the future, I create this testing code.
        # But currently, the column doesn't exists to judge the race conditions
        pass

    def test_get_race_result_with_horse_age_param(self):
        """Testing to get the DataFrame with horse age parameters
        """
        # [TODO]
        # In the future, I create this testing code.
        # But currently, the column doesn't exists to judge the horse age
        pass

    def test_get_race_result_with_grade_param(self):
        """Testing to get the DataFrame with grade parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.START_YEAR: 2019,
            netkeiba.url_params.GRADE: ["G2"]
        }
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert all(["2" in name for name in df["grade"].to_list()])

    def test_get_race_result_with_distance_from_param(self):
        """Testing to get the DataFrame with distance_from parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.START_YEAR: 2019,
            netkeiba.url_params.DISTANCE_FROM: 3000
        }
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert all([int(val) >= 3000 for val in df["distance"].to_list()])

    def test_get_race_result_with_distance_to_param(self):
        """Testing to get the DataFrame with distance_from parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.START_YEAR: 2019,
            netkeiba.url_params.DISTANCE_TO: 2000
        }
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert all([int(val) <= 2000 for val in df["distance"].to_list()])

    def test_get_race_result_with_start_year_params(self):
        """Testing to get the DataFrame with start-year parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.START_YEAR: 2018,
            netkeiba.url_params.END_YEAR: 2019
        }
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert any([2018 == dt.year for dt in df["date"].to_list()])

    def test_get_race_result_with_start_year_params(self):
        """Testing to get the DataFrame with end-year parameters
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.START_YEAR: 2019,
            netkeiba.url_params.END_YEAR: 2019
        }
        df = netkeiba.get_race_result(params)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0
        assert any([2019 == dt.year for dt in df["date"].to_list()])

    def test_get_race_details_with_correct_url(self):
        """Testing to get the DataFrame of horse racing details data
        """
        details_url = "https://db.netkeiba.com/race/201906050811/"
        df = netkeiba.get_race_details(details_url)
        assert not (df is None)
        assert type(df) == pd.DataFrame
        assert len(df) > 0

    def test_get_race_details_with_wrong_url(self):
        """Testing to get the None value not a DataFrame
        """
        details_url = "https://db.netkeiba.com/race/202206050811/"
        df = netkeiba.get_race_details(details_url)
        assert df is None

    def test_get_race_details_with_wrong_url(self):
        """Testing to occurred error to set wrong URL string
        """
        details_url = "test/test/test"
        with self.assertRaises(requests.exceptions.MissingSchema):
            df = netkeiba.get_race_details(details_url)