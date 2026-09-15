import heapq
import random
from ..cell import Cell
from ..grid import Grid
from ..direction import Direction
from .protocol import MazeAlgorithm
from dataclasses import dataclass, field


class Prim(MazeAlgorithm):
    """Implements a randomized Prim's maze generation strategy."""

    def execute(self, grid: Grid) -> None:
        """Carve paths by growing a minimum spanning tree with random weights.

        Starts from the top-left cell and repeatedly expands the cheapest
        frontier edge, assigning each candidate neighbor a random cost.
        Every popped cell is connected back to the cell that discovered it,
        producing a spanning tree over the grid. Returns early if the grid
        has no cell at (0, 0).

        Args:
            grid: The initialized grid matrix to modify.
        """
        start_cell = grid.get_cell(0, 0)
        if start_cell is None:
            return
        min_heap: list[Edge] = []
        heapq.heappush(min_heap, Edge(weight=-1, cell=start_cell))
        prev: dict[Cell, Cell] = {}
        costs: dict[Cell, int] = {start_cell: -1}
        while min_heap:
            edge = heapq.heappop(min_heap)
            current = edge.cell
            if current.visited:
                continue
            current.visited = True
            predecessor = prev.get(current)
            if predecessor is not None:
                vector = (current.x - predecessor.x, current.y - predecessor.y)
                direction = Direction.vector_direction(vector)
                grid.connect_cells(predecessor, current, direction)
            unvisited_neighbors = grid.get_unvisited_neighbors(current)
            for _, neighbor in unvisited_neighbors:
                cost = random.randint(0, 100)
                if (neighbor not in costs or cost < costs[neighbor]):
                    costs[neighbor] = cost
                    prev[neighbor] = current
                    heapq.heappush(min_heap, Edge(cost, neighbor))


@dataclass(order=True)
class Edge:
    """A weighted reference to a cell, ordered by weight.

    Wraps a cell together with the random cost of reaching it so that
    instances can be stored in a min-heap. All comparisons delegate to
    the weight; the cell itself is never part of the ordering.

    Attributes:
        weight: The cost of the edge leading to the cell.
        cell: The cell this edge points to (ignored in comparisons).
    """
    weight: int
    cell: Cell = field(compare=False)
