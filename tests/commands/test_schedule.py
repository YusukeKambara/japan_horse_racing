import unittest
import zipfile
from datetime import datetime
from src.commands import schedule as commands_schedule

class TestSchedule(unittest.TestCase):
    """Test class for testing the commands.schedule module
    
    Arguments:
        unittest {[type]} -- [description]
    """

    @classmethod
    def setUpClass(cls):
        print("*" * 80 + "\nStart to test [commands.schedule] module\n" + "*" * 80)

    def test_get_with_invaild_year_race_name(self):
        """Testing to occurred error if the argument's year is invaild
        """
        with self.assertRaises(zipfile.BadZipFile):
            commands_schedule.get(9999, False)
        with self.assertRaises(zipfile.BadZipFile):
            commands_schedule.get(9999, True)

    def test_get_of_race_name(self):
        """Testing to be able to get the raca name data in this year
        """
        current_year = datetime.now().year
        race_name_data = commands_schedule.get(current_year, False)
        assert len(race_name_data) != 0
        assert race_name_data[0]["date"].year == current_year
        assert race_name_data[0]["title"] != ""

    def test_get_of_place(self):
        """Testing to be able to get the place to open the event
        """
        current_year = datetime.now().year
        race_name_data = commands_schedule.get(current_year, True)
        assert len(race_name_data) != 0
        assert race_name_data[0]["date"].year == current_year
        assert "競馬" in race_name_data[0]["title"]