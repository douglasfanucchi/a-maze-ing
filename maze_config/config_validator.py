import os
import re


class ConfigValidator:
    """Validate the configuration file and its syntax."""
    def __init__(self, path: str) -> None:
        self.path = path

    def file_exists(self) -> bool:
        """Check whether a file exists.

        Args:
            path: The path of the file to be checked.

        Returns:
            True if a file exists, False otherwise.
        """
        return os.path.isfile(self.path)

    def is_readable(self) -> bool:
        """Check whether a file is readable.

        Args:
            path: The path of the file to check permissions.

        Returns:
            True if file has reading permissions, False otherwise.
        """
        return os.access(self.path, os.R_OK)

    @staticmethod
    def is_valid_line(line: str) -> bool:
        """Check whether a given line has valid configuration syntax.

        Args:
            line: A string that represents a line in the configuration file.

        Returns:
            True if line has a valid syntax, False otherwise.
        """
        stripped = line.strip()
        if len(stripped) == 0:
            return True
        if stripped.startswith("#"):
            return True
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=[^\s=]+(\s+#.*)?$", stripped):
            return True
        return False

    def is_valid_file_syntax(self) -> bool:
        """Check whether all lines have valid syntax.

        Args:
            path: The path of the file to have its lines checked.

        Returns:
            True if the syntax of all lines are valid, False otherwise.
        """
        with open(self.path, "r") as config_file:
            return all(
                ConfigValidator.is_valid_line(line) for line in config_file
            )
