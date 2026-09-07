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

    @classmethod
    def direction_vector(cls, direction: Direction) -> tuple[int, int]:
        """Return the vector that moves a point into a certain direction"""
        vectors: dict[Direction, tuple] = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0)
        }
        return vectors[direction]

    @classmethod
    def vector_direction(cls, vector: tuple[int, int]) -> Direction:
        """Return the direction that is associated with a vector"""
        directions: dict[tuple, Direction] = {
            (0, -1): Direction.NORTH,
            (1, 0): Direction.EAST,
            (0, 1): Direction.SOUTH,
            (-1, 0): Direction.WEST
        }
        return directions[vector]

    @classmethod
    def get_direction_label(cls, direction: Direction) -> str:
        """
        Return the cardinal abreviation of a given direction.
        """
        labels: dict[Direction, str] = {
            Direction.NORTH: "N",
            Direction.EAST: "E",
            Direction.SOUTH: "S",
            Direction.WEST: "W",
        }
        return labels[direction]
