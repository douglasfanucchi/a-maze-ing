from typing import Protocol
from mazegen.grid import Grid
from typing import Optional


class MazeAlgorithm(Protocol):
    """Defines the strict interface for maze generation algorithms."""

    def __init__(self, seed: Optional[int]):
        """Initiate the algorithm default state.
        
        Args:
            seed: Seed to reproduce a specific paths creation.
        """
        ...

    def execute(self, grid: Grid) -> None:
        """Execute the spanning tree algorithm to carve paths.

        Args:
            grid: The initialized grid containing unvisited cells.
        """
        ...
