import random
from ..grid import Grid
from ..cell import Cell
from ..direction import Direction
from .protocol import MazeAlgorithm


class Kruskal(MazeAlgorithm):
    """Implements a randomized kruskal's maze generation strategy."""
    def execute(self, grid: Grid) -> None:
        """Carve paths using Kruskal's minimum spanning tree algorithm.

        Extracts all valid interior walls, randomizes their order, and iterates
        through them. It uses a disjoint-set data structure to connect adjacent
        cells only if they do not already share a path, preventing loops.

        Args:
            grid: The initialized grid matrix to modify.
        """
        uf: UnionFind = UnionFind(grid.cells_list)
        walls: list[tuple[Cell, Cell, Direction]] = grid.get_walls()
        random.shuffle(walls)
        for cell_1, cell_2, direction in walls:
            if uf.union(cell_1, cell_2):
                grid.connect_cells(cell_1, cell_2, direction)


class UnionFind:
    """Manages connected components for Kruskal's algorithm."""
    def __init__(self, all_cells: list[Cell]) -> None:
        """Initialize the dictionary with each cell as its own root."""
        self.parent: dict[Cell, Cell] = {cell: cell for cell in all_cells}

    def find(self, cell: Cell) -> Cell:
        """Find the root of the cell's set and compress the path."""
        if self.parent[cell] != cell:
            self.parent[cell] = self.find(self.parent[cell])
        return self.parent[cell]

    def union(self, cell_1: Cell, cell_2: Cell) -> bool:
        """Merge two sets. Returns True if they were disjoint."""
        root1 = self.find(cell_1)
        root2 = self.find(cell_2)
        if root1 != root2:
            self.parent[root2] = root1
            return True
        return False
