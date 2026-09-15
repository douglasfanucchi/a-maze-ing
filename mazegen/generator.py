from mazegen.grid import Grid
from mazegen.algorithms.protocol import MazeAlgorithm
from mazegen.direction import Direction
from mazegen.cell import Cell


class MazeGenerator:
    """Orchestrate the maze generation sequence and output formatting.

    Manages grid initialization constraints, reserves center coordinates for
    the 42 school pattern, delegates path carving to a strategy algorithm,
    and handles post-processing loop generation for playable mazes.

    Attributes:
        grid (Grid): The spatial grid matrix containing cells and walls.
        algorithm (MazeAlgorithm): The strategy instance used to carve paths.
        is_perfect (bool): Flag determining if the maze remains a strict tree
            or includes loops.
        entry (tuple[int, int]): Starting coordinates (x, y).
        exit (tuple[int, int]): Ending coordinates (x, y).
    """

    def __init__(
        self,
        grid: Grid,
        entry_coords: tuple[int, int],
        exit_coords: tuple[int, int],
        algorithm: MazeAlgorithm,
        is_perfect: bool = False
    ) -> None:
        """Initialize the maze generator with grid constraints and strategies.

        Args:
            grid: The pre-allocated grid matrix to modify.
            entry_coords: The (x, y) coordinates where traversal begins.
            exit_coords: The (x, y) coordinates where traversal ends.
            algorithm: The generation strategy conforming to MazeAlgorithm.
            is_perfect: If True, generates a single-solution tree. If False,
                removes dead-ends to introduce loops.

        Raises:
            ValueError: If entry and exit coordinates match, or if either
                coordinate falls outside the grid boundaries.
        """
        if entry_coords == exit_coords:
            raise ValueError("ENTRY and EXIT must be different.")
        if (entry_coords[0] < 0 or entry_coords[0] >= grid.width
                or entry_coords[1] < 0 or entry_coords[1] >= grid.height):
            raise ValueError("ENTRY coordinates are out of bounds.")
        if (exit_coords[0] < 0 or exit_coords[0] >= grid.width
                or exit_coords[1] < 0 or exit_coords[1] >= grid.height):
            raise ValueError("EXIT coordinates are out of bounds.")
        self.grid = grid
        self.algorithm = algorithm
        self.is_perfect = is_perfect
        self.entry = entry_coords
        self.exit = exit_coords

    def generate(self) -> None:
        """Execute maze generation sequence."""
        self._reserve_42_pattern()
        self.algorithm.execute(self.grid)
        if not self.is_perfect:
            self._create_loops()

    def export(self) -> str:
        """Create output containing maze configuration.

        Returns:
            A string containing maze hexadecimal representation, its dimensions
            and the entry and exit coordinates.
        """
        result = ""
        for y in range(0, self.grid.height):
            line = ""
            for x in range(0, self.grid.width):
                cell = self.grid.get_cell(x, y)
                if cell is None:
                    continue
                line += cell.to_hex()
            result += line + "\n"
        result += f"\n{self.entry[0]},{self.entry[1]}\n"
        result += f"{self.exit[0]},{self.exit[1]}"
        return result

    def render(self) -> None:
        """Generate and display a visual representation of the maze."""
        # Generates visual representation of the maze
        ...

    def _reserve_42_pattern(self) -> None:
        """Reserve center cells for the 42 pattern by marking them visited.

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
                            "overlaps with the entry or exit coordinate at "
                            f"({block_x}, {block_y})."
                        )
                    cell = self.grid.get_cell(block_x, block_y)
                    if cell is not None:
                        cell.visited = True
                        cell.forty_two = True

    def _create_loops(self) -> None:
        """Create loops for a playable maze by removing dead-ends."""
        for row in self.grid.matrix:
            for cell in row:
                if cell is None or cell.count_walls() != 3:
                    continue
                for direction in Direction:
                    if self._can_break_wall(cell, direction):
                        neighbor = self.grid.get_neighbor(cell, direction)
                        if neighbor is not None:
                            self.grid.connect_cells(cell, neighbor, direction)
                            break

    def _can_break_wall(self, cell: Cell, direction: Direction) -> bool:
        """Check if a wall can be safely broken in a given direction.

        Args:
            cell: The origin cell attempting to expand.
            direction: The cardinal direction to check.

        Returns:
            True if a wall exists and target neighbor also exists
            and is not part of the reserved 42 pattern, False otherwise.
        """
        to_connect: Cell | None = self.grid.get_neighbor(cell, direction)
        return (
            cell.has_wall(direction) and
            to_connect is not None and
            to_connect.forty_two is False
        )
