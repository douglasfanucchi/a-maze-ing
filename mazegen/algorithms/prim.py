import random
from ..grid import Grid
from ..cell import Cell
from ..direction import Direction
from .protocol import MazeAlgorithm
import heapq
from ..edge import Edge


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
        min_heap: list[Edge] = list()
        current = grid.get_cell(0, 0)
        if current is None:
            return
        prev: list[list[Cell | None]] = [
            [
                None for _ in row
            ] for row in grid.matrix
        ]
        costs: list[list[int]] = [
            [
                -1 for _ in row
            ] for row in grid.matrix
        ]
        heapq.heappush(min_heap, Edge(-1, current))
        while len(min_heap):
            edge = heapq.heappop(min_heap)
            current = edge.cell
            if current.visited:
                continue
            current.visited = True
            antecessor = prev[edge.cell.y][edge.cell.x]
            if antecessor is not None:
                grid.connect_cells(
                    antecessor,
                    current,
                    Direction.vector_direction(
                        (current.x - antecessor.x,
                            current.y - antecessor.y)
                    )
                )
            unvisited_neighbors = grid.get_unvisited_neighbors(current)
            for _, neighbor in unvisited_neighbors:
                cost = random.randint(0, 100)
                if (costs[neighbor.y][neighbor.x] == -1
                        or cost < costs[neighbor.y][neighbor.x]):
                    heapq.heappush(min_heap, Edge(cost, neighbor))
                    prev[neighbor.y][neighbor.x] = current
                    costs[neighbor.y][neighbor.x] = cost
