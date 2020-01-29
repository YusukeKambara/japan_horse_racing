import unittest
from datasource.netkeiba import io as netkeiba
from src.commands import race as commands_race

class TestRace(unittest.TestCase):
    """Test class for testing the commands.race module
    
    Arguments:
        unittest {[type]} -- [description]
    """
    
    @classmethod
    def setUpClass(cls):
        print("*" * 80 + "\nStart to test [commands.race] module\n" + "*" * 80)

    def test_get_result_with_invaild_params(self):
        """Testing to occurred error if the argument's params are invaild
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.WORD: None,
            netkeiba.url_params.START_YEAR: 9999,
            netkeiba.url_params.START_MONTH: None,
            netkeiba.url_params.END_YEAR: None,
            netkeiba.url_params.END_MONTH: None
        }
        assert commands_race.get_result(params) is None

    def test_get_result_with_race_name(self):
        """Testing to occurred error if the argument's params are invaild
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.WORD: "有馬記念",
            netkeiba.url_params.START_YEAR: None,
            netkeiba.url_params.START_MONTH: None,
            netkeiba.url_params.END_YEAR: None,
            netkeiba.url_params.END_MONTH: None
        }
        df = commands_race.get_result(params)
        assert all(["有馬記念" in race_name for race_name in df["race_name"].to_list()])

    def test_get_result_with_two_years(self):
        """Testing to occurred error if the argument's params are invaild
        """
        params = {
            netkeiba.url_params.PID: netkeiba.pid_list.RACE_LIST,
            netkeiba.url_params.WORD: "有馬記念",
            netkeiba.url_params.START_YEAR: 2018,
            netkeiba.url_params.START_MONTH: None,
            netkeiba.url_params.END_YEAR: 2019,
            netkeiba.url_params.END_MONTH: None
        }
        df = commands_race.get_result(params)
        assert any([dt.year == 2018 for dt in df["date"].to_list()])
        assert any([dt.year == 2019 for dt in df["date"].to_list()])