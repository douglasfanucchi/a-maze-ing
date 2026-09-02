from mazegen.direction import Direction


class Cell:
    def __init__(self, x: int, y: int) -> None:
        if x < 0 or y < 0:
            raise ValueError(f"Invalid coordinates: ({x}, {y})")
        self._x = x
        self._y = y
        self._walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }

    def get_x(self) -> int:
        return self._x

    def get_y(self) -> int:
        return self._y

    def break_wall(self, side: str) -> None:
        if side not in self._walls:
            raise ValueError(f"Invalid side: {side}")
        self._walls[side] = False

    def has_wall(self, side: str) -> bool:
        if side not in self._walls:
            raise ValueError(f"Invalid side: {side}")
        return self._walls[side]

    def to_bitmask(self) -> int:
        bitmask = 0
        if self._walls["N"]:
            bitmask |= Direction.NORTH
        if self._walls["E"]:
            bitmask |= Direction.EAST
        if self._walls["S"]:
            bitmask |= Direction.SOUTH
        if self._walls["W"]:
            bitmask |= Direction.WEST
        return bitmask

    def to_hex(self) -> str:
        return format(self.to_bitmask(), "x")
