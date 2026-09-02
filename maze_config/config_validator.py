import os
import re


class ConfigValidator:
    def __init__(self, path: str) -> None:
        self._path = path

    @staticmethod
    def file_exists(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def is_readable(path: str) -> bool:
        return os.access(path, os.R_OK)

    @classmethod
    def is_valid_line(cls, line: str) -> bool:
        stripped = line.strip()
        if len(stripped) == 0:
            return True
        if stripped.startswith("#"):
            return True
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=\S+(\s+#.*)?$", stripped):
            return True
        return False

    @classmethod
    def is_valid_file_syntax(cls, path: str) -> bool:
        with open(path, "r") as config_file:
            return all(cls.is_valid_line(line) for line in config_file)
