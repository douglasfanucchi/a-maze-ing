from .protocol import MazeAlgorithm
from mazegen.grid import Grid
from mazegen.cell import Cell
import random
from collections import deque


class DepthFirstSearch(MazeAlgorithm):
    """Implements a randomized Depth-First Search maze generation strategy."""
    def execute(self, grid: Grid) -> None:
        """Carve paths using a randomized DFS stack.

        Args:
            grid: The initialized grid matrix to modify.
        """
        stack: deque[Cell] = deque()
        start_cell = grid.get_cell(0, 0)
        if start_cell is None:
            return
        start_cell.visited = True
        stack.append(start_cell)
        while stack:
            curr = stack[-1]
            curr.visited = True
            unvisited_neighbors = grid.get_unvisited_neighbors(curr)
            if unvisited_neighbors:
                direction, neighbor = random.choice(unvisited_neighbors)
                grid.connect_cells(curr, neighbor, direction)
                stack.append(neighbor)
            else:
                stack.pop()
