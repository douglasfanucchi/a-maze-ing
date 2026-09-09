from enum import IntEnum


class Direction(IntEnum):
    """Represent cardinal directions for maze generation and solving.

    Inherits from IntEnum to assign bitwise integer values (powers of two)
    to each direction. This structure allows efficient wall management within
    the grid, where a single integer can represent multiple wall combinations
    using bitwise operations.

    Attributes:
        NORTH (int): The northern direction flag (1).
        EAST (int): The eastern direction flag (2).
        SOUTH (int): The southern direction flag (4).
        WEST (int): The western direction flag (8).
    """
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def opposite(self) -> "Direction":
        """Return the cardinal opposite of the current direction."""
        opposites = {
            Direction.NORTH: Direction.SOUTH,
            Direction.SOUTH: Direction.NORTH,
            Direction.EAST: Direction.WEST,
            Direction.WEST: Direction.EAST,
        }
        return opposites[self]

    @property
    def vector(self) -> tuple[int, int]:
        """Return the vector that moves a point into a certain direction."""
        vectors: dict[Direction, tuple[int, int]] = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0)
        }
        return vectors[self]

    @staticmethod
    def vector_direction(vector: tuple[int, int]) -> "Direction":
        """Return the direction that is associated with a vector."""
        directions: dict[tuple[int, int], Direction] = {
            (0, -1): Direction.NORTH,
            (1, 0): Direction.EAST,
            (0, 1): Direction.SOUTH,
            (-1, 0): Direction.WEST
        }
        return directions[vector]

    @property
    def label(self) -> str:
        """Return the cardinal abreviation of a given direction."""
        labels: dict[Direction, str] = {
            Direction.NORTH: "N",
            Direction.EAST: "E",
            Direction.SOUTH: "S",
            Direction.WEST: "W",
        }
        return labels[self]
