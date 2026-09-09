import random
from ..grid import Grid
from ..cell import Cell
from ..direction import Direction
from .protocol import MazeAlgorithm


class HuntAndKill(MazeAlgorithm):
    """Implements a randomized Hunt and Kill maze generation strategy."""
    def execute(self, grid: Grid) -> None:
        """Carve paths using the Hunt and Kill algorithm.

        Alternates between a random walk (kill phase) and a linear scan
        (hunt phase). Utilizes a flattened grid list to optimize the scan
        and specifically avoids connecting to the reserved 42 pattern.

        Args:
            grid: The initialized grid matrix to modify.
        """
        current: Cell | None = grid.get_cell(0, 0)
        if current is None:
            return
        current.visited = True
        hunt_index: int = 0
        while current is not None:
            # --- Kill phase (Random walk) ---
            while True:
                neighbors = grid.get_unvisited_neighbors(current)
                if not neighbors:
                    break  # Dead-end reached, transition to hunt phase
                direction, neighbor = random.choice(neighbors)
                grid.connect_cells(current, neighbor, direction)
                neighbor.visited = True
                current = neighbor
            # --- Hunt phase (linear scan) ---
            current = None
            for i in range(hunt_index, len(grid.cells_list)):
                cell = grid.cells_list[i]
                if not cell.visited:
                    visited_neighbors = self.get_visited_neighbors(grid, cell)
                    if visited_neighbors:
                        direction, neighbor = random.choice(visited_neighbors)
                        grid.connect_cells(cell, neighbor, direction)
                        cell.visited = True
                        current = cell
                        hunt_index = i
                        break

    def get_visited_neighbors(
        self, grid: Grid, cell: Cell
    ) -> list[tuple[Direction, Cell]]:
        """Find valid, visited adjacent cells outside the 42 pattern.

        Args:
            grid: The maze grid being processed.
            cell: The unvisited cell seeking a connection.

        Returns:
            A list of tuples containing the Direction and the visited Cell.
        """
        valid_neighbors: list[tuple[Direction, Cell]] = []
        for direction in Direction:
            neighbor = grid.get_neighbor(cell, direction)
            if (
                neighbor is not None
                and neighbor.visited
                and not neighbor.forty_two
            ):
                valid_neighbors.append((direction, neighbor))
        return valid_neighbors
