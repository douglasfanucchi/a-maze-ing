from mazegen.grid import Grid
from mazegen.cell import Cell
from collections import deque
from mazegen.direction import Direction


class Solver:
    """Find shortest path from entry to exit of a given maze grid.

    Traverses the maze with a breadth-first search to find the shortest path.
    Path is stored as a string of cardinal labels ("N", "E", "S", "W"), each
    character being one step taken from the entry cell.

    Attributes:
        _grid: The Grid holding the maze cells and their walls.
        _entry_coords: The (x, y) coordinates where every path starts.
        _exit_coords: The (x, y) coordinates every complete path ends at.
        shortest_path: The shortest path found from entry to exit.
    """

    def __init__(
        self,
        grid: Grid,
        entry_coords: tuple[int, int],
        exit_coords: tuple[int, int]
    ):
        """Initiate Solver states and find shortest path using BFS algorithm.

        Args:
            grid: The Grid containing the generated maze to traverse.
            entry_coords: The (x, y) coordinates where the traversal starts.
            exit_coords: The (x, y) coordinates the traversal targets.
        """
        self._grid: Grid = grid
        self._entry_coords: tuple[int, int] = entry_coords
        self._exit_coords: tuple[int, int] = exit_coords
        self.shortest_path: str = ""
        self.shortest_path_cells: list[Cell] = []
        self._bfs()

    def _bfs(self) -> None:
        """Traverse the maze breadth-first to find the shortest path.

        Explores the grid from the entry cell, crossing only the sides where
        a wall was removed. The search halts immediately upon discovering the
        exit cell, guaranteeing the resulting path is the shortest possible.
        """
        start_cell = self._grid.get_cell(*self._entry_coords)
        if start_cell is None:
            return
        queue: deque[Cell] = deque([start_cell])
        prev: dict[Cell, Cell] = {start_cell: start_cell}
        while queue:
            v = queue.popleft()
            if (v.x, v.y) == self._exit_coords:
                self.shortest_path = self._backtrack_path(v, prev)[0]
                self.shortest_path_cells = self._backtrack_path(v, prev)[1]
                return
            for direction in Direction:
                if v.has_wall(direction):
                    continue
                w = self._grid.get_neighbor(v, direction)
                if w is None:
                    continue
                if w not in prev:
                    prev[w] = v
                    queue.append(w)

    def _backtrack_path(
        self, current: Cell, prev: dict[Cell, Cell]
    ) -> tuple[str, list[Cell]]:
        """Rebuild the path walked from the entry up to a given cell.

        Args:
            current: The cell to backtrack from, the last step of the path.
            prev: The matrix of predecessors filled by the search, where the
                entry cell is its own predecessor and marks the path start.

        Returns:
            A string of cardinal labels describing each step taken from the
            entry to the given cell, ordered from the first step.
        """
        result_str: list[str] = []
        result_cells: list[Cell] = [current]
        while prev[current] != current:
            previous = prev[current]
            vector = (current.x - previous.x, current.y - previous.y)
            direction = Direction.vector_direction(vector)
            result_str.append(direction.label)
            current = previous
            result_cells.append(current)
        result_str.reverse()
        result_cells.reverse()
        return ("".join(result_str), result_cells)
