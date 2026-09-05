from .config_validator import ConfigValidator
from re import match, search
from typing import Callable
from os import access, W_OK, path


class Config:
    """Load, validate and expose values from a maze configuration file.

    The configuration file is expected to be a plain text file with
    ``KEY=value`` lines (optionally followed by a ``# comment``), one of
    each of the required keys: ``WIDTH``, ``HEIGHT``, ``ENTRY``, ``EXIT``,
    ``OUTPUT_FILE`` and ``PERFECT``.
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
        self._valid_keys: list[str] = [
            key for key in self._required_keys
        ]
        self._values: dict[str, int | tuple[int, int] | str | bool] = {}
        self._path: str = path
        self._validate_config_file()
        self._raw_values: dict[str, str] = self._get_raw_values()
        self._validate_config_values()
        self._load_values()

    def get(self, key: str) -> int | tuple[int, int] | str | bool:
        """Return the parsed value for a configuration key.

        Args:
            key: The configuration key to look up (e.g. ``"WIDTH"``).

        Returns:
            The parsed and type-converted value for the given key.

        Raises:
            ValueError: If the key is not a valid configuration key.
        """
        if key not in self._values:
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
        if not ConfigValidator.file_exists(self._path):
            raise FileNotFoundError("Config file does not exist.")
        if not ConfigValidator.is_readable(self._path):
            raise PermissionError("Config file has no read permission.")
        if not ConfigValidator.is_valid_file_syntax(self._path):
            raise ValueError("Invalid syntax on configuration file.")
        missing_keys: list[str] = self._get_missing_required_keys()
        if len(missing_keys):
            raise ValueError(
                f"Missing {", ".join(missing_keys)} key"
                + f"{"s" if len(missing_keys) > 1 else ""}."
            )

    def _get_missing_required_keys(self) -> list[str]:
        """Find which required keys are absent from the config file.

        Returns:
            The required keys that have no corresponding ``KEY=value``
            line in the config file.
        """
        presented_keys = {key: False for key in self._required_keys}

        with open(self._path, "r", encoding="utf-8") as config_file:
            for line in config_file:
                for key in presented_keys:
                    if match(f"^{key}=[^\\s#]{{1,}}", line):
                        presented_keys[key] = True
            return [key for key in presented_keys if not presented_keys[key]]

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
        positive_number_regex: str = "[1-9][0-9]{1,}"
        rules_list: dict[str, list[Callable[[str], bool]]] = {
            "WIDTH": [
                lambda value: bool(match(f"^{positive_number_regex}$", value))
            ],
            "HEIGHT": [
                lambda value: bool(match(f"^{positive_number_regex}$", value))
            ],
            "ENTRY": [
                lambda value: bool(match("^0,0$", value)),
                lambda value: bool(
                    match(f"^0,{positive_number_regex}$", value)
                ),
                lambda value: bool(
                    match(f"^{positive_number_regex},0$", value)
                ),
                lambda value: bool(match(
                    f"^{positive_number_regex},{positive_number_regex}$",
                    value
                ))
            ],
            "EXIT": [
                lambda value: bool(match("^0,0$", value)),
                lambda value: bool(
                    match(f"^0,{positive_number_regex}$", value)
                ),
                lambda value: bool(
                    match(f"^{positive_number_regex},0$", value)
                ),
                lambda value: bool(match(
                    f"^{positive_number_regex},{positive_number_regex}$",
                    value
                ))
            ],
            "OUTPUT_FILE": [
                lambda value: bool(
                    (path.isfile(value) and access(value, W_OK)) or
                    (not path.isfile(value)
                        and access(path.dirname(value), W_OK))
                )
            ],
            "PERFECT": [
                lambda value: bool(match("^(True|False)$", value))
            ]
        }

        for key in self._raw_values:
            value = self._raw_values[key]
            rules = rules_list[key]
            if not any(rule(value) for rule in rules):
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
