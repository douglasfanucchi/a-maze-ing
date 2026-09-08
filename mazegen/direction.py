from enum import IntEnum


class Direction(IntEnum):
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
        """Return the vector that moves a point into a certain direction"""
        vectors: dict[Direction, tuple[int, int]] = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0)
        }
        return vectors[self]

    @staticmethod
    def vector_direction(vector: tuple[int, int]) -> "Direction":
        """Return the direction that is associated with a vector"""
        directions: dict[tuple[int, int], Direction] = {
            (0, -1): Direction.NORTH,
            (1, 0): Direction.EAST,
            (0, 1): Direction.SOUTH,
            (-1, 0): Direction.WEST
        }
        return directions[vector]

    @property
    def label(self) -> str:
        """
        Return the cardinal abreviation of a given direction.
        """
        labels: dict[Direction, str] = {
            Direction.NORTH: "N",
            Direction.EAST: "E",
            Direction.SOUTH: "S",
            Direction.WEST: "W",
        }
        return labels[self]
