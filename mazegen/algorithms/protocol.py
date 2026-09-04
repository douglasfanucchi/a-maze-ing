from typing import Protocol
from mazegen.grid import Grid


class MazeAlgorithm(Protocol):
    """Defines the strict interface for maze generation algorithms."""

    def execute(self, grid: Grid) -> None:
        """Execute the spanning tree algorithm to carve paths.

        Args:
            grid: The initialized grid containing unvisited cells.
        """
        ...
