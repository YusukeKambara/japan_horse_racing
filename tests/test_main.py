import datetime
import logging
import unittest
from click.testing import CliRunner
from src import main


class TestMain(unittest.TestCase):
    """Test class for testing the main module

    Arguments:
        unittest {[type]} -- [description]
    """

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
        result = self.runner.invoke(main.cmd, ["nondifined"])
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
        result = self.runner.invoke(main.schedule, ["nondifined"])
        assert result.exit_code == 2
        assert "No such command" in result.output

    def test_main_schedule_command_with_get_command(self):
        """Testing for the main function with schedule command with get command
        """
        result = self.runner.invoke(main.schedule, ["get"])
        assert result.exit_code == 0
        assert type(eval(result.output)) is list