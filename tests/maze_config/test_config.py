import pytest
from pathlib import Path
from maze_config import Config
from os.path import abspath


class TestConfig:
    @pytest.fixture
    def config_file_with_invalid_syntax(self, tmp_path: Path):
        content: str = (
            "# This is a valid comment\n"
            "0INVALID_IDENTIFIER=123 # comment\n"
            "VALID_IDENTIFIER=\n"
        )
        file_path = tmp_path / "invalid.txt"
        file_path.write_text(content)
        yield file_path
        file_path.unlink()

    @pytest.fixture
    def unreadable_config_file(self, tmp_path: Path):
        file_path = tmp_path / "unreadable.txt"
        file_path.write_text("")
        file_path.chmod(0o000)
        yield file_path
        file_path.unlink()

    @pytest.fixture
    def config_file(self, tmp_path: Path):
        file_path = tmp_path / "config.txt"
        file_path.write_text((
            "# config file\n"
            "\n"
            "WIDTH=20 # maze width\n"
            "HEIGHT=15 # maze height\n"
            "ENTRY=0,0 # maze entry\n"
            "EXIT=19,14 # maze exit\n"
            "OUTPUT_FILE=maze.txt # maze output file\n"
            "PERFECT=True # maze perfect\n"
        ))
        yield file_path
        file_path.unlink()

    @pytest.fixture
    def config_file_missing_required_keys(self, tmp_path: Path):
        file_path = tmp_path / "missing_keys.txt"
        file_path.write_text((
            "# WIDTH=20\n"
            "# HEIGHT=15\n"
            "# ENTRY=0,0\n"
            "# EXIT=19,14\n"
            "# OUTPUT_FILE=maze.txt\n"
            "# PERFECT=True\n"
            "SEED=123\n"
            "ALGO=DFS\n"
            "ANIMATED=False\n"
        ))
        yield file_path
        file_path.unlink()

    @pytest.fixture
    def config_file_with_key_name_prefix_collision(self, tmp_path: Path):
        file_path = tmp_path / "prefix_collision.txt"
        file_path.write_text((
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "OUTPUT_FILENAME=maze.txt\n"
            "PERFECT=True\n"
        ))
        yield file_path
        file_path.unlink()

    @pytest.fixture
    def config_file_with_empty_output_file_value(self, tmp_path: Path):
        file_path = tmp_path / "empty_output_value.txt"
        file_path.write_text((
            "WIDTH=20\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=19,14\n"
            "OUTPUT_FILE=#comment\n"
            "PERFECT=True\n"
        ))
        yield file_path
        file_path.unlink()

    @pytest.fixture
    def non_writable_dir(self, tmp_path: Path):
        dir_path = tmp_path / "non_writable_dir"
        dir_path.mkdir()
        dir_path.chmod(0o000)
        yield dir_path
        dir_path.rmdir()

    def test_should_instantiate_config_object_with_non_existing_file(self):
        with pytest.raises(FileNotFoundError):
            Config("/non/existing/file.txt")

    def test_should_instantiate_config_object_with_non_readable_file(
            self,
            unreadable_config_file
    ):
        with pytest.raises(PermissionError):
            Config(str(unreadable_config_file))

    def test_should_instantiate_config_object_with_invalid_file(
            self,
            config_file_with_invalid_syntax
    ):
        with pytest.raises(ValueError):
            Config(str(config_file_with_invalid_syntax))

    def test_should_instantiate_config_object_with_file_missing_required_keys(
        self,
        config_file_missing_required_keys
    ):
        required = "WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT"
        with pytest.raises(
            ValueError,
            match=f"Missing {required} keys."
        ):
            Config(str(config_file_missing_required_keys))

    def test_should_instantiate_config_object_with_key_name_prefix_collision(
        self,
        config_file_with_key_name_prefix_collision
    ):
        with pytest.raises(
            ValueError,
            match="Missing OUTPUT_FILE key."
        ):
            Config(str(config_file_with_key_name_prefix_collision))

    def test_should_instantiate_config_object_with_empty_output_file_value(
        self,
        config_file_with_empty_output_file_value
    ):
        with pytest.raises(
            ValueError,
            match="Missing OUTPUT_FILE key."
        ):
            Config(str(config_file_with_empty_output_file_value))

    @pytest.mark.parametrize("invalid_width", [-1, 0])
    def test_should_instantiate_config_object_with_invalid_width(
        self,
        invalid_width,
        config_file
    ):
        content = config_file.read_text()
        content = content.replace("WIDTH=20", f"WIDTH={invalid_width}")
        config_file.write_text(content)

        with pytest.raises(
            ValueError,
            match="Invalid value for WIDTH key."
        ):
            Config(str(config_file))

    @pytest.mark.parametrize("invalid_height", [-1, 0])
    def test_should_instantiate_config_object_with_invalid_height(
        self,
        invalid_height,
        config_file
    ):
        content = config_file.read_text()
        content = content.replace("HEIGHT=15", f"HEIGHT={invalid_height}")
        config_file.write_text(content)

        with pytest.raises(
            ValueError,
            match="Invalid value for HEIGHT key."
        ):
            Config(str(config_file))

    @pytest.mark.parametrize(
        "invalid_entry",
        ["-1,-1", "-1,0", "0,-1", "zero,0", "0,zero", "zero,zero", "any_text"]
    )
    def test_should_instantiate_config_object_with_invalid_entry(
        self,
        invalid_entry,
        config_file
    ):
        content = config_file.read_text()
        content = content.replace("ENTRY=0,0", f"ENTRY={invalid_entry}")
        config_file.write_text(content)

        with pytest.raises(
            ValueError,
            match="Invalid value for ENTRY key"
        ):
            Config(str(config_file))

    @pytest.mark.parametrize(
        "invalid_exit",
        ["-1,-1", "-1,0", "0,-1", "zero,0", "0,zero", "zero,zero", "any_text"]
    )
    def test_should_instantiate_config_object_with_invalid_exit(
        self,
        invalid_exit,
        config_file
    ):
        content = config_file.read_text()
        content = content.replace("EXIT=19,14", f"EXIT={invalid_exit}")
        config_file.write_text(content)

        with pytest.raises(
            ValueError,
            match="Invalid value for EXIT key"
        ):
            Config(str(config_file))

    def test_should_instantiate_config_object_with_non_writable_output_file(
        self,
        config_file,
        tmp_path,
    ):
        non_writable_path = tmp_path / "non_writable.txt"
        non_writable_path.write_text("")
        non_writable_path.chmod(0o000)
        content = config_file.read_text().replace(
            "OUTPUT_FILE=maze.txt", f"OUTPUT_FILE={str(non_writable_path)}"
        )
        config_file.write_text(content)

        with pytest.raises(
            ValueError,
            match="Invalid value for OUTPUT_FILE key."
        ):
            Config(str(config_file))

    def test_should_instantiate_config_object_with_non_writable_directory(
        self,
        config_file,
        non_writable_dir
    ):
        content = config_file.read_text().replace(
            "OUTPUT_FILE=maze.txt",
            f"OUTPUT_FILE={str(non_writable_dir / 'output.txt')}",
        )
        config_file.write_text(content)

        with pytest.raises(
            ValueError,
            match="Invalid value for OUTPUT_FILE key."
        ):
            Config(str(config_file))

    @pytest.mark.parametrize("invalid_perfect_value", ["any"])
    def test_should_instantiate_config_object_with_perfect_invalid_values(
            self,
            config_file,
            invalid_perfect_value
    ):
        content = config_file.read_text().replace(
            "PERFECT=True",
            f"PERFECT={invalid_perfect_value}",
        )
        config_file.write_text(content)

        with pytest.raises(
            ValueError,
            match="Invalid value for PERFECT key."
        ):
            Config(str(config_file))

    def test_should_instantiate_config_object_with_uknown_keys(
        self,
        config_file
    ):
        content = config_file.read_text() + "NEW_KEY=123"
        config_file.write_text(content)
        config = Config(str(config_file))

        assert isinstance(config, Config)

    def test_should_instantiate_object_with_valid_values(
        self,
        config_file
    ):
        config = Config(str(config_file))

        assert isinstance(config, Config)
        assert config.get("WIDTH") == 20
        assert config.get("HEIGHT") == 15
        assert config.get("ENTRY") == (0, 0)
        assert config.get("EXIT") == (19, 14)
        assert config.get("OUTPUT_FILE") == abspath("maze.txt")
        assert config.get("PERFECT") is True

    def test_should_get_invalid_key_from_config(self, config_file):
        config = Config(str(config_file))

        with pytest.raises(
            ValueError,
            match="Invalid key TEST"
        ):
            config.get("TEST")

    def test_should_get_seed_config_with_a_positive_value(self, config_file):
        content = config_file.read_text()
        config_file.write_text(content + "SEED=1\n")

        config = Config(str(config_file))

        assert config.get("SEED") == 1

    def test_should_get_seed_config_with_zero_value(self, config_file):
        content = config_file.read_text()
        config_file.write_text(content + "SEED=0\n")

        config = Config(str(config_file))

        assert config.get("SEED") == 0

    def test_should_get_seed_config_with_negative_value(self, config_file):
        content = config_file.read_text()
        config_file.write_text(content + "SEED=-1\n")

        config = Config(str(config_file))

        assert config.get("SEED") == -1

    def test_should_get_none_for_seed_when_getting_it_without_specifying_value(
        self,
        config_file
    ):
        config = Config(str(config_file))

        assert config.get("SEED") is None

    @pytest.mark.parametrize(
        "setting_value, expected",
        [
            ("ON", True),
            ("OFF", False)
        ]
    )
    def test_should_get_value_of_animations_option(
        self,
        config_file,
        setting_value,
        expected
    ):
        content = config_file.read_text()
        config_file.write_text(content + f"ANIMATIONS={setting_value}")

        config = Config(str(config_file))

        assert config.get("ANIMATIONS") is expected

    def test_should_get_false_when_getting_animations_wihtout_specifying(
        self,
        config_file
    ):
        config = Config(str(config_file))

        assert config.get("ANIMATIONS") is False

    @pytest.mark.parametrize(
        "algorithm",
        [
            ("DFS"),
            ("Prim")
        ]
    )
    def test_should_get_algorithm_setting_from_config_file(
        self,
        algorithm,
        config_file
    ):
        content = config_file.read_text()
        config_file.write_text(content + f"ALGORITHM={algorithm}")

        config = Config(str(config_file))

        assert config.get("ALGORITHM") == algorithm

    def test_should_get_dfs_algorithm_when_setting_is_not_specified(
        self,
        config_file
    ):
        config = Config(str(config_file))

        assert config.get("ALGORITHM") == "DFS"
