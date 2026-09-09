from mazegen.cell import Cell
from mazegen.direction import Direction


class Grid:
    """Represents a 2D matrix of Cell objects for the maze.

    Handles spatial boundaries, coordinate validation and neighbor discovery.

    Attributes:
        width: The total number of columns in the grid.
        height: The total number of rows in the grid.
        matrix: A 2D list containing the instantiated Cell objects.
        cells_list: The flattened list version of matrix
    """

    def __init__(self, width: int, height: int) -> None:
        """Initialize a Grid instance with the specified dimensions.

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
        self.matrix = self.create_matrix()
        self.cells_list = [cell for row in self.matrix for cell in row]

    def create_matrix(self) -> list[list[Cell]]:
        """Generate a 2D array populated with unvisited Cell instances.

        Returns:
            A nested list representing the matrix grid.
        """
        matrix: list[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)] for y in range(self.height)
        ]
        return matrix

    def get_cell(self, x: int, y: int) -> Cell | None:
        """Retrieve a Cell safely from the matrix using its coordinates.

        Args:
            x: The horizontal coordinate to search.
            y: The vertical coordinate to search.

        Returns:
            The Cell instance if coordinates are within bounds, otherwise None.
        """
        if (not 0 <= x < self.width) or (not 0 <= y < self.height):
            return None
        return self.matrix[y][x]

    def get_neighbor(self, cell: Cell, direction: Direction) -> Cell | None:
        """Retrieve neighbor of cell in a particular direction if it exists.

        Args:
            cell: Current node from which to find neighbor
            direction: Direction to look for neighbor

        Returns:
            The adjacent cell instance in that direction from current cell
            if it exists, otherwise None
        """
        dx, dy = direction.vector
        return self.get_cell(cell.x + dx, cell.y + dy)

    def get_walls(self) -> list[tuple[Cell, Cell, Direction]]:
        """Retrieve list of all walls separating valid cells.

        Returns: A list of tuples (cell, neighbor, direction)
        representing all internal walls excluding the 42 pattern
        """
        walls: list[tuple[Cell, Cell, Direction]] = []
        for row in self.matrix:
            for cell in row:
                if cell.visited:
                    continue
                for direction in (Direction.EAST, Direction.SOUTH):
                    neighbor = self.get_neighbor(cell, direction)
                    if neighbor is not None and not neighbor.visited:
                        walls.append((cell, neighbor, direction))
        return walls

    def get_unvisited_neighbors(
        self, cell: Cell
    ) -> list[tuple[Direction, Cell]]:
        """Find valid, unvisited adjacent cells within the grid boundaries.

        Args:
            cell: The current node being processed.

        Returns:
            A list of tuples containing the Direction to the neighbor
            and the neighbor Cell.
        """
        neighbors: list[tuple[Direction, Cell]] = []
        for direction in Direction:
            neighbor_cell = self.get_neighbor(cell, direction)
            if (neighbor_cell is not None) and (not neighbor_cell.visited):
                neighbors.append((direction, neighbor_cell))
        return neighbors

    def connect_cells(
        self, current: Cell, neighbor: Cell, direction: Direction
    ) -> None:
        """Remove the walls between two adjacent cells bidirectionally.

        Args:
            current: The starting cell node.
            neighbor: The adjacent cell node to connect to.
            direction: The cardinal direction moving from current to neighbor.

        Raises:
            ValueError: If the cells are not actually adjacent neighbors.
        """
        # Validate the cells are strictly 1 step apart (Manhattan distance = 1)
        dx = abs(current.x - neighbor.x)
        dy = abs(current.y - neighbor.y)
        if (dx + dy) != 1:
            current_coords: str = f"({current.x}, {current.y})"
            neighbor_coords: str = f"({neighbor.x}, {neighbor.y}))"
            cells: str = f"{current_coords} and {neighbor_coords}"
            raise ValueError(f"Cannot connect non-adjacent cells: {cells}")
        current.remove_wall(direction)
        neighbor.remove_wall(direction.opposite)
