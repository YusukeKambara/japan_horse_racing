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