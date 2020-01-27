import unittest
from tests import test_main
from tests.utils import test_utils
from tests.commands import test_schedule


def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(test_main.TestMain))
  suite.addTests(unittest.makeSuite(test_utils.TestUtils))
  suite.addTests(unittest.makeSuite(test_schedule.TestSchedule))
  return suite