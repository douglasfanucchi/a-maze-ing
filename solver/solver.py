from mazegen.grid import Grid
from mazegen.cell import Cell
from collections import deque
from mazegen.direction import Direction


class Solver:
    """Generate paths from entry to exit of a given maze represented by a Grid.

    Traverses the maze once with a breadth-first search and classifies every
    branch it walks into complete paths, shortest paths, dead-ends and loops.
    Paths are stored as strings of cardinal labels ("N", "E", "S", "W"), each
    character being one step taken from the entry cell.

    Attributes:
        _grid: The Grid holding the maze cells and their walls.
        _entry_coords: The (x, y) coordinates where every path starts.
        _exit_coords: The (x, y) coordinates every complete path ends at.
        _paths: Every path found from entry to exit, shortest first.
        _shortest_paths: The subset of paths sharing the minimum length.
        _wrong_paths: Paths that end on a dead-end cell instead of the exit.
        _loops: Paths that reach a cell already discovered by the search.
    """

    def __init__(
        self,
        grid: Grid,
        entry_coords: tuple[int, int],
        exit_coords: tuple[int, int]
    ):
        """Initiate Solver states and find paths using BFS algorithm.

        Args:
            grid: The Grid containing the generated maze to traverse.
            entry_coords: The (x, y) coordinates where the traversal starts.
            exit_coords: The (x, y) coordinates the traversal targets.
        """
        self._grid: Grid = grid
        self._entry_coords: tuple[int, int] = entry_coords
        self._exit_coords: tuple[int, int] = exit_coords
        self._paths: list[str] = []
        self._shortest_paths: list[str] = []
        self._wrong_paths: list[str] = []
        self._loops: list[str] = []
        self._bfs()
        self._update_shortest_paths()

    @property
    def paths(self) -> list[str]:
        """Return every complete path found from the entry to the exit.

        Returns:
            A list of strings of cardinal labels, ordered from the shortest
            to the longest path.
        """
        return self._paths

    @property
    def shortest_paths(self) -> list[str]:
        """Return the complete paths tied at the minimum length.

        Returns:
            A list of strings of cardinal labels, all of the same length.
        """
        return self._shortest_paths

    @property
    def wrong_paths(self) -> list[str]:
        """Return the paths that end on a dead-end instead of the exit.

        Returns:
            A list of strings of cardinal labels, each ending on a cell
            surrounded by three walls.
        """
        return self._wrong_paths

    @property
    def loops(self) -> list[str]:
        """Return the paths that reach a cell already discovered.

        Returns:
            A list of strings of cardinal labels, each ending on the cell
            where the loop was detected.
        """
        return self._loops

    def _bfs(self) -> None:
        """Traverse the maze breadth-first and classify each branch walked.

        Explores the grid from the entry cell, crossing only the sides where
        a wall was removed, and fills the internal path lists: complete paths
        when the exit is reached, wrong paths when a dead-end is reached and
        loops when an already discovered cell is reached again. Does nothing
        when the entry coordinates fall outside the grid.
        """
        start_cell = self._grid.get_cell(*self._entry_coords)
        if start_cell is None:
            return
        queue: deque[Cell] = deque([start_cell])
        prev: dict[Cell, Cell] = {start_cell: start_cell}
        while queue:
            v = queue.popleft()
            if (v.x, v.y) == self._exit_coords:
                self._paths.append(self._backtrack_path(v, prev))
                del prev[v]
                continue
            for direction in Direction:
                if v.has_wall(direction):
                    continue
                w = self._grid.get_neighbor(v, direction)
                if w is None:
                    continue
                if prev.get(v) == w:
                    if v.count_walls() == 3:
                        self._wrong_paths.append(self._backtrack_path(v, prev))
                    continue
                if w in prev:
                    self._loops.append(self._backtrack_path(v, prev))
                    continue
                prev[w] = v
                queue.append(w)

    def _backtrack_path(self, current: Cell, prev: dict[Cell, Cell]) -> str:
        """Rebuild the path walked from the entry up to a given cell.

        Args:
            v: The cell to backtrack from, the last step of the path.
            prev: The matrix of predecessors filled by the search, where the
                entry cell is its own predecessor and marks the path start.

        Returns:
            A string of cardinal labels describing each step taken from the
            entry to the given cell, ordered from the first step.
        """
        result: list[str] = []
        while prev[current] != current:
            previous = prev[current]
            if previous is None:
                break
            vector = (current.x - previous.x, current.y - previous.y)
            direction = Direction.vector_direction(vector)
            result.append(direction.label)
            current = previous
        result.reverse()
        return "".join(result)

    def _update_shortest_paths(self) -> None:
        """Collect the complete paths that share the shortest length.

        Relies on the paths being stored in non-decreasing length order by
        the search, so it keeps the leading paths until a longer one is
        found. Does nothing when no complete path was found.
        """
        if len(self._paths) == 0:
            return
        self._shortest_paths.append(self._paths[0])
        shortest_len = len(self._shortest_paths[0])
        for i in range(1, len(self._paths)):
            if len(self._paths[i]) > shortest_len:
                break
            self._shortest_paths.append(self._paths[i])
