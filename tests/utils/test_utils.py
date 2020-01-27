from os.path import basename
import unittest
from src.utils import utils

class TestUtils(unittest.TestCase):
    """Test class for testing the utils module
    
    Arguments:
        unittest {[type]} -- [description]
    """
    
    def test_get_project_root(self):
        """Testing to be able to get the project root pathname
        """
        assert "japan_horse_racing" == basename(utils.get_project_root())