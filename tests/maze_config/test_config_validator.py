import pytest

from maze_config.config_validator import ConfigValidator
from pathlib import Path


class TestConfigValidator:
    @pytest.fixture
    def valid_config_file(self, tmp_path: Path):
        content = (
            "# Maze dimensions\n"
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "# Entry and exit coordinates\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "# Output settings\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
        )
        file_path = tmp_path / "config.txt"
        file_path.write_text(content)
        return file_path

    @pytest.fixture
    def unreadable_config_file(self, tmp_path: Path):
        file_path = tmp_path / "unreadable_config.txt"
        file_path.write_text("WIDTH=20\n")
        file_path.chmod(0o000)
        yield file_path
        file_path.chmod(0o644)

    def test_should_return_false_when_file_does_not_exist(self):
        assert ConfigValidator.file_exists("non_existing_file.txt") is False

    def test_should_return_true_when_file_exists(self, valid_config_file):
        assert ConfigValidator.file_exists(str(valid_config_file)) is True

    def test_should_return_true_when_file_is_readable(
        self, valid_config_file
    ):
        assert ConfigValidator.is_readable(str(valid_config_file)) is True

    def test_should_return_false_when_file_is_not_readable(
        self, unreadable_config_file
    ):
        path = str(unreadable_config_file)

        assert ConfigValidator.is_readable(path) is False

    def test_is_valid_line_should_return_true_for_a_line_that_is_a_comment(
        self,
    ):
        line = "# This is just a comment\n"

        assert ConfigValidator.is_valid_line(line) is True

    def test_is_valid_line_should_return_true_for_a_key_value_pair(self):
        line = "WIDTH=20\n"

        assert ConfigValidator.is_valid_line(line) is True

    def test_is_valid_line_should_return_false_for_an_invalid_indetifier(
        self,
    ):
        line = "0WIDTH=20\n"

        assert ConfigValidator.is_valid_line(line) is False

    def test_is_valid_line_should_return_true_for_valid_pair_and_comment(
        self,
    ):
        line = "WIDTH=20      #This is just a comment"

        assert ConfigValidator.is_valid_line(line) is True

    def test_is_valid_line_should_return_false_for_pair_with_invalid_char(
        self,
    ):
        line = "WIDTH=20      -"

        assert ConfigValidator.is_valid_line(line) is False

    def test_is_valid_line_should_return_true_for_an_empty_line(self):
        assert ConfigValidator.is_valid_line("") is True
        assert ConfigValidator.is_valid_line("\n") is True

    def test_should_check_for_a_valid_syntax_in_a_file(
        self, valid_config_file
    ):
        path = str(valid_config_file)

        assert ConfigValidator.is_valid_file_syntax(path) is True

    def test_should_check_for_invalid_line_with_double_equal_sign(self):
        assert ConfigValidator.is_valid_line("WIDTH==20") is False
