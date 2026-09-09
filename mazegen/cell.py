from mazegen.direction import Direction


class Cell:
    """Represents a single cell node within a maze grid.

    Tracks coordinates, wall state using a bitmask, and traversal history.

    Attributes:
        x: Zero-based horizontal coordinate of the cell. (Starts from left)
        y: Zero-based vertical coordinate of the cell. (Starts from top)
        walls: Bitmask integer representing wall states (0 to 15).
        visited: Boolean flag tracking if the cell was already processed.
    """

    def __init__(self, x: int, y: int) -> None:
        """Initialize a Cell instance with coordinates and closed walls.

        Args:
            x: The horizontal coordinate.
            y: The vertical coordinate.

        Raises:
            ValueError: If coordinates are negative.
        """
        if x < 0 or y < 0:
            raise ValueError(f"Invalid coordinates: ({x}, {y})")
        self.x: int = x
        self.y: int = y
        self.forty_two: bool = False
        self.walls: int = 15  # Binary 1111 (all walls closed)
        self.visited: bool = False

    def __eq__(self, other: object) -> bool:
        """Check if two cells are logically identical based on coordinates."""
        if not isinstance(other, Cell):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Generate a unique hash using the immutable coordinate tuple."""
        return hash((self.x, self.y))

    def remove_wall(self, direction: Direction) -> None:
        """Remove a wall in the specified cardinal direction.

        Args:
            direction: The cardinal direction enum corresponding to the wall.
        """
        self.walls &= ~direction.value

    def has_wall(self, direction: Direction) -> bool:
        """Check if a wall exists in the specified direction.

        Args:
            direction: The cardinal direction enum to verify.

        Returns:
            True if the wall is closed, False otherwise.
        """
        return bool(self.walls & direction.value)

    def to_hex(self) -> str:
        """Convert the wall bitmask into a single hexadecimal character.

        Returns:
            A lowercase string with 1 hex char representing the cell's walls.
        """
        return format(self.walls, "x")

    def count_walls(self) -> int:
        """Count the number of active walls around the cell.

        Returns:
            The total number of walls (from 0 to 4).
        """
        return self.walls.bit_count()
