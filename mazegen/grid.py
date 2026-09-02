from mazegen.cell import Cell
from mazegen.direction import Direction


class Grid:
    """
    Represents a 2D matrix of Cell objects for the maze.

    Handles spatial boundaries, coordinate validation and neighbor discovery.

    Attributes:
        width: The total number of columns in the grid.
        height: The total number of rows in the grid.
        matrix: A 2D list containing the instantiated Cell objects.
    """

    def __init__(self, width: int, height: int) -> None:
        """
        Initialize a Grid instance with the specified dimensions.

        Args:
            width: The total number of columns in the grid.
            height: The total number of rows in the grid.

        Raises:
            ValueError: If either width or height is not positive.
        """
        if width <= 0 or height <= 0:
            dimensions: str = f"(WIDTH={width}, HEIGHT={height})"
            raise ValueError(f"Invalid dimensions: {dimensions}")
        self.width = width
        self.height = height
        self.matrix: list[list[Cell]] = self.create_matrix()

    def create_matrix(self) -> list[list[Cell]]:
        """
        Generate a 2D array populated with unvisited Cell instances.

        Returns:
            A nested list representing the matrix grid.
        """
        matrix: list[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        return matrix

    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Retrieve a Cell safely from the matrix using its coordinates.

        Args:
            x: The horizontal coordinate to search.
            y: The vertical coordinate to search.

        Returns:
            The Cell instance if coordinates are within bounds, otherwise None.
        """
        if (not 0 <= x < self.width) or (not 0 <= y < self.height):
            return None
        return self.matrix[y][x]

    def get_unvisited_neighbors(
        self, cell: Cell
    ) -> list[tuple[Direction, Cell]]:
        """
        Find valid, unvisited adjacent cells within the grid boundaries.

        Args:
            cell: The current node being processed.

        Returns:
            A list of tuples containing the Direction to the neighbor
            and the neighbor Cell.
        """
        neighbors: list[tuple[Direction, Cell]] = []
        # Map cardinal directions to (dx, dy) coordinate offsets
        offsets: dict[Direction, tuple[int, int]] = {
            Direction.NORTH: (0, -1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, 1),
            Direction.WEST: (-1, 0),
        }
        for direction, (dx, dy) in offsets.items():
            neighbor_x = cell.x + dx
            neighbor_y = cell.y + dy
            neighbor_cell = self.get_cell(neighbor_x, neighbor_y)
            if (neighbor_cell is not None) and (not neighbor_cell.visited):
                neighbors.append((direction, neighbor_cell))
        return neighbors
