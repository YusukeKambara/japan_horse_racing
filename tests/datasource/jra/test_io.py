import unittest
import zipfile
from datetime import datetime
from src.datasource.jra import io as jra

class TestIo(unittest.TestCase):
    """Test class for testing the jra datasource
    
    Arguments:
        unittest {[type]} -- [description]
    """

    @classmethod
    def setUpClass(cls):
        print("*" * 80 + "\nStart to test [datasource.jra] module\n" + "*" * 80)

    def test_get_race_name_list_with_invalid_argument_year(self):
        """Testing to occurred error if the argument's year is invaild
        """
        with self.assertRaises(zipfile.BadZipFile):
            jra.get_race_name_list(9999, False)
        with self.assertRaises(zipfile.BadZipFile):
            jra.get_race_name_list(9999, True)

    def test_get_race_name_list(self):
        """Testing to be able to get the raca name data in this year
        """
        current_year = datetime.now().year
        race_name_data = jra.get_race_name_list(current_year, False)
        assert len(race_name_data) != 0
        assert race_name_data[0]["date"].year == current_year
        assert race_name_data[0]["title"] != ""

    def test_get_race_name_list_with_place_option(self):
        """Testing to be able to get the place to open the event
        """
        current_year = datetime.now().year
        race_name_data = jra.get_race_name_list(current_year, True)
        assert len(race_name_data) != 0
        assert race_name_data[0]["date"].year == current_year
        assert "競馬" in race_name_data[0]["title"]