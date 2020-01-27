import unittest
from tests import test_main
from tests.utils import test_utils
from tests.commands import test_schedule
from tests.datasource.jra import test_io as test_jra


def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(test_main.TestMain))
  suite.addTests(unittest.makeSuite(test_utils.TestUtils))
  suite.addTests(unittest.makeSuite(test_schedule.TestSchedule))
  suite.addTests(unittest.makeSuite(test_jra.TestIo))
  return suite