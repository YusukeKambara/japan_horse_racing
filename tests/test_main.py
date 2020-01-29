import datetime
import logging
import unittest
import pandas as pd
from click.testing import CliRunner
import main
from datasource.netkeiba import io as netkeiba


class TestMain(unittest.TestCase):
    """Test class for testing the main module

    Arguments:
        unittest {[type]} -- [description]
    """

    @classmethod
    def setUpClass(cls):
        print("*" * 80 + "\nStart to test [main] module\n" + "*" * 80)

    def setUp(self):
        self.runner = CliRunner()

    def test_main_no_command(self):
        """Testing for the main function with no argument
        """
        result = self.runner.invoke(main.cmd, [])
        assert result.exit_code == 0
        assert "First layer sub-command group" in result.output

    def test_main_non_defined_command(self):
        """Testing for the main function with non-defined command at first layer
        """
        result = self.runner.invoke(main.cmd, ["nondefined"])
        assert result.exit_code == 2
        assert "No such command" in result.output

    def test_main_schedule_command_without_child_command(self):
        """Testing for the main function with schedule command without child command
        """
        result = self.runner.invoke(main.cmd, ["schedule"])
        assert result.exit_code == 0
        assert "Second layer sub-command group" in result.output

    def test_main_schedule_command_with_non_defined_command(self):
        """Testing for the main function with schedule command with non-defined command
        """
        result = self.runner.invoke(main.schedule, ["nondefined"])
        assert result.exit_code == 2
        assert "No such command" in result.output

    def test_main_schedule_command_with_get_command(self):
        """Testing for the main function with schedule command with get command
        """
        result = self.runner.invoke(main.schedule, ["get"])
        assert result.exit_code == 0
        assert type(eval(result.output)) is list

    def test_main_race_command_without_child_command(self):
        """Testing for the main function with race command without child command
        """
        result = self.runner.invoke(main.cmd, ["race"])
        assert result.exit_code == 0
        assert "Second layer sub-command group" in result.output

    def test_main_race_command_with_non_defined_command(self):
        """Testing for the main function with race command with non-defined command
        """
        result = self.runner.invoke(main.race, ["nondefined"])
        assert result.exit_code == 2
        assert "No such command" in result.output

    def test_main_race_command_with_get_command(self):
        """Testing for the main function with race command with get command
        """
        result = self.runner.invoke(main.race, ["get-result"])
        assert result.exit_code == 0
        assert all([header in result.output for header in netkeiba.RACE_RESULT_HEADER])