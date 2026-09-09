from .config_validator import ConfigValidator
from re import match, search
from typing import Callable, Literal, overload
from os import access, W_OK, path


class Config:
    """Load, validate and expose values from a maze configuration file.

    The configuration file is expected to be a plain text file with
    ``KEY=value`` lines (optionally followed by a ``# comment``), one of
    each of the required keys: ``WIDTH``, ``HEIGHT``, ``ENTRY``, ``EXIT``,
    ``OUTPUT_FILE``, ``ANIMATIONS``, ``ALGORITHM``, ``SEED`` and ``PERFECT``.
    """

    def __init__(self, path: str):
        """Load and validate the configuration file at the given path.

        Args:
            path: The path of the configuration file to load.

        Raises:
            FileNotFoundError: If the config file does not exist.
            PermissionError: If the config file has no read permission.
            ValueError: If the config file has invalid syntax, is missing
                required keys, or has an invalid value for a known key.
        """
        self._required_keys: list[str] = [
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
        ]
        self._optional_keys: dict[str, None | bool | int | str] = {
            "SEED": None,
            "ANIMATIONS": False,
            "ALGORITHM": "DFS",
        }
        self._valid_keys: list[str] = (
            self._required_keys + list(self._optional_keys.keys())
        )
        self._values: dict[str, int | tuple[int, int] | str | bool] = {}
        self._path: str = path
        self._validate_config_file()
        self._raw_values: dict[str, str] = self._get_raw_values()
        self._validate_config_values()
        self._load_values()

    @overload
    def get(self, key: Literal["WIDTH", "HEIGHT"]) -> int:
        ...

    @overload
    def get(self, key: Literal["SEED"]) -> int | None:
        ...

    @overload
    def get(self, key: Literal["ENTRY", "EXIT"]) -> tuple[int, int]:
        ...

    @overload
    def get(self, key: Literal["OUTPUT_FILE", "ALGORITHM"]) -> str:
        ...

    @overload
    def get(self, key: Literal["PERFECT", "ANIMATIONS"]) -> bool:
        ...

    @overload
    def get(self, key: str) -> int | tuple[int, int] | str | bool | None:
        ...

    def get(self, key: str) -> int | tuple[int, int] | str | bool | None:
        """Return the parsed value for a configuration key.

        Args:
            key: The configuration key to look up (e.g. ``"WIDTH"``).

        Returns:
            The parsed and type-converted value for the given key.

        Raises:
            ValueError: If the key is not a valid configuration key.
        """
        if key not in self._values:
            if key in self._optional_keys:
                return self._optional_keys[key]
            else:
                raise ValueError(f"Invalid key {key}")
        return self._values[key]

    def _validate_config_file(self) -> None:
        """Validate the config file's existence, permissions and content.

        Raises:
            FileNotFoundError: If the config file does not exist.
            PermissionError: If the config file has no read permission.
            ValueError: If the config file has invalid syntax or is
                missing required keys.
        """
        validator = ConfigValidator(self._path)
        if not validator.file_exists():
            raise FileNotFoundError("Config file does not exist.")
        if not validator.is_readable():
            raise PermissionError("Config file has no read permission.")
        if not validator.is_valid_file_syntax():
            raise ValueError("Invalid syntax on configuration file.")
        missing_keys: list[str] = self._get_missing_required_keys()
        if len(missing_keys):
            raise ValueError(
                f"Missing {', '.join(missing_keys)} key"
                + f"{'s' if len(missing_keys) > 1 else ''}."
            )

    def _get_missing_required_keys(self) -> list[str]:
        """Find which required keys are absent from the config file.

        Returns:
            The required keys that have no corresponding ``KEY=value``
            line in the config file.
        """
        missing_keys = {key: True for key in self._required_keys}

        with open(self._path, "r", encoding="utf-8") as config_file:
            for line in config_file:
                for key in missing_keys:
                    if match(f"^{key}=[^\\s#]{{1,}}", line):
                        missing_keys[key] = False
            return [key for key, missing in missing_keys.items() if missing]

    def _get_raw_values(self) -> dict[str, str]:
        """Parse each recognized key's value out of the config file.

        Returns:
            A mapping of recognized config keys to their raw (still
            string, not yet type-converted) values, with ``OUTPUT_FILE``
            resolved to an absolute path.
        """
        raw_values: dict[str, str] = {}
        with open(self._path, "r") as config_file:
            for line in config_file:
                stripped = line.strip()
                if stripped.startswith("#") or len(stripped) == 0:
                    continue
                result = search("(?P<key>.*)=(?P<value>[^#\\s]*)", stripped)
                if result is None:
                    continue
                key = result.group("key")
                if key not in self._valid_keys:
                    continue
                value = result.group("value")
                raw_values[key] = value
            raw_values["OUTPUT_FILE"] = path.abspath(raw_values["OUTPUT_FILE"])
            return raw_values

    def _validate_config_values(self) -> None:
        """Check every raw config value against its key's validation rules.

        Raises:
            ValueError: If any key's raw value fails all of its rules.
        """
        pos_num_regex: str = r"[1-9][0-9]*"
        coordinate_regex: str = r"^(0|[1-9][0-9]*),(0|[1-9][0-9]*)$"
        rules: dict[str, Callable[[str], bool]] = {
            "WIDTH": lambda value: bool(match(f"^{pos_num_regex}$", value)),
            "HEIGHT": lambda value: bool(match(f"^{pos_num_regex}$", value)),
            "ENTRY": lambda value: bool(match(coordinate_regex, value)),
            "EXIT": lambda value: bool(match(coordinate_regex, value)),
            "OUTPUT_FILE":
                lambda value: bool(
                    (path.isfile(value) and access(value, W_OK)) or
                    (not path.isfile(value)
                        and access(path.dirname(value), W_OK))
                ),
            "PERFECT":
                lambda value: bool(match("^(True|False)$", value)),
            "SEED": lambda value: bool(match(r"^[-]?([1-9][0-9]*|0)$", value)),
            "ANIMATIONS":
                lambda value: bool(match("^(ON|OFF)$", value)),
            "ALGORITHM":
                lambda value: bool(match("^(DFS|Prim)$", value)),
        }

        for key in self._raw_values:
            value = self._raw_values[key]
            rule = rules[key]
            if not rule(value):
                raise ValueError(f"Invalid value for {key} key.")

    def _load_values(self) -> None:
        """Type-convert the raw config values into their final values."""
        self._values["WIDTH"] = int(self._raw_values["WIDTH"])
        self._values["HEIGHT"] = int(self._raw_values["HEIGHT"])
        tuple_values: list[str] = self._raw_values["ENTRY"].split(",")
        self._values["ENTRY"] = (int(tuple_values[0]), int(tuple_values[1]))
        tuple_values = self._raw_values["EXIT"].split(",")
        self._values["EXIT"] = (int(tuple_values[0]), int(tuple_values[1]))
        self._values["OUTPUT_FILE"] = self._raw_values["OUTPUT_FILE"]
        self._values["PERFECT"] = self._raw_values["PERFECT"] == "True"
        if "SEED" in self._raw_values:
            self._values["SEED"] = int(self._raw_values["SEED"])
        if "ANIMATIONS" in self._raw_values:
            self._values["ANIMATIONS"] = self._raw_values["ANIMATIONS"] == "ON"
        if "ALGORITHM" in self._raw_values:
            self._values["ALGORITHM"] = self._raw_values["ALGORITHM"]
