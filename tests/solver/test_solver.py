from typing import Callable

import pytest

from solver import Solver
from mazegen import MazeGenerator
from mazegen.grid import Grid
from mazegen.algorithms import DFS


@pytest.fixture
def generate_maze() -> Callable[[int, int, bool], MazeGenerator]:
    def _generate_maze(
        width: int, height: int, is_perfect: bool = False
    ) -> MazeGenerator:
        grid = Grid(width, height)
        generator = MazeGenerator(
            grid=grid,
            entry_coords=(0, 0),
            exit_coords=(width - 1, height - 1),
            algorithm=DFS(1000),
            is_perfect=is_perfect
        )
        generator.generate()
        return generator
    return _generate_maze


class TestSolver:
    def test_should_solve_a_simple_2x2_maze(
        self, generate_maze: Callable[[int, int, bool], MazeGenerator]
    ) -> None:
        generator = generate_maze(2, 2, True)
        solver = Solver(generator.grid)
        # 1011 1011
        # 1100 0110

        assert len(solver.paths()) == 1
        assert len(solver.shortest_paths()) == 1
        assert len(solver.wrong_paths()) == 0
        assert solver.shortest_paths()[0] == "SE"
