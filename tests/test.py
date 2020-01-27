import unittest
from tests import test_main


def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(test_main.TestMain))
  return suite