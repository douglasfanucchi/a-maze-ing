from .protocol import MazeAlgorithm
from mazegen.grid import Grid
from mazegen.cell import Cell
from typing import Optional
import random
from collections import deque


class DFS(MazeAlgorithm):
    def __init__(self, seed: Optional[int] = None):
        random.seed(seed)

    def execute(self, grid: Grid) -> None:
        stack: deque[Cell] = deque()
        stack.append(grid.get_cell(0, 0))
        while len(stack):
            v = stack[-1]
            v.visited = True
            nodes = grid.get_unvisited_neighbors(v)
            if len(nodes) > 0:
                idx = random.randint(0, len(nodes) - 1)
                w = nodes[idx][1]
                grid.connect_cells(v, w, nodes[idx][0])
                stack.append(w)
            else:
                stack.pop()
