from mazegen.grid import Grid
from mazegen.algorithms.protocol import MazeAlgorithm
from mazegen.direction import Direction
from mazegen.cell import Cell


class MazeGenerator():
    """
    """

    def __init__(
        self,
        grid: Grid,
        entry_coords: tuple[int, int],
        exit_coords: tuple[int, int],
        algorithm: MazeAlgorithm,
        is_perfect: bool = False
    ) -> None:
        """
        """
        self.grid = grid
        self.algorithm = algorithm
        self.is_perfect = is_perfect
        self.entry = entry_coords
        self.exit = exit_coords

    def generate(self) -> None:
        """Execute maze generation sequence"""
        self._reserve_42_pattern()
        self.algorithm.execute(self.grid)
        if not self.is_perfect:
            self._create_loops()

    def export(self) -> str:
        """
        Create output containing maze configuration.

        Returns:
            A string containing maze hexadecimal representation, its dimensions
            and the coordinates to the shortes path from entry to end.
        """
        result = ""
        for y in range(0, self.grid.height):
            line = ""
            for x in range(0, self.grid.width):
                line += self.grid.get_cell(x, y).to_hex()
            result += line + "\n"
        result += f"\n{self.entry[0]},{self.entry[1]}\n"
        result += f"{self.exit[0]},{self.exit[1]}"
        return result

    def render(self) -> None:
        """
        """
        # Generates visual representation of the maze
        ...

    def _reserve_42_pattern(self) -> None:
        """
        Reserve center cells for the 42 pattern by marking them visited.

        Raises:
            ValueError: If width or height is too small to fit the 42 pattern
        """
        pattern_width = 7
        pattern_height = 5
        min_width = pattern_width + 2
        min_height = pattern_height + 2

        # Validate the grid is large enough to hold the pattern safely
        if (self.grid.width < min_width or self.grid.height < min_height):
            raise ValueError(
                f"Grid size ({self.grid.width}x{self.grid.height})"
                f" is too small for the 42 pattern. Minimum required: "
                f"{min_width}x{min_height}."
            )

        # (start_x, start_y) are the top left coordinates
        # where the 42 pattern starts
        start_x = (self.grid.width - pattern_width) // 2
        start_y = (self.grid.height - pattern_height) // 2

        # 2D list representing the specific blocked cells for "42"
        # (1 means reserved, 0 means normal cell)
        pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        for dy, row in enumerate(pattern):
            for dx, block in enumerate(row):
                if block == 1:
                    block_x: int = start_x + dx
                    block_y: int = start_y + dy
                    if (block_x, block_y) in [self.entry, self.exit]:
                        raise ValueError(
                            "Configuration overlap: The 42 pattern "
                            "overlaps wiith the entry or exit coordinate at "
                            f"({block_x}, {block_y})."
                        )
                    cell = self.grid.get_cell(block_x, block_y)
                    if cell is not None:
                        cell.visited = True
                        cell.forty_two = True

    def _create_loops(self) -> None:
        """
        Create loops for a playable maze by removing dead-ends.
        """
        for y in range(0, self.grid.height):
            for x in range(0, self.grid.width):
                cell = self.grid.get_cell(x, y)
                if cell is None or cell.count_walls() != 3:
                    continue
                direction: Direction | None = None
                for i in range(0, 4):
                    if self._can_break_wall(cell, Direction(1 << i)):
                        direction = Direction(1 << i)
                if direction is None:
                    continue
                new_x: int = cell.x + Direction.direction_vector(direction)[0]
                new_y: int = cell.y + Direction.direction_vector(direction)[1]
                to_connect = self.grid.get_cell(new_x, new_y)
                if to_connect is None:
                    continue
                self.grid.connect_cells(cell, to_connect, direction)

    def _can_break_wall(self, cell: Cell, direction: Direction) -> bool:
        x: int = cell.x + Direction.direction_vector(direction)[0]
        y: int = cell.y + Direction.direction_vector(direction)[1]
        to_connect: Cell | None = self.grid.get_cell(x, y)
        return (
            cell.has_wall(direction) and
            to_connect is not None and
            to_connect.forty_two is False
        )
