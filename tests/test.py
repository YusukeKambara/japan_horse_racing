import unittest
from tests import test_main
from tests.utils import test_utils


def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(test_main.TestMain))
  suite.addTests(unittest.makeSuite(test_utils.TestUtils))
  return suite