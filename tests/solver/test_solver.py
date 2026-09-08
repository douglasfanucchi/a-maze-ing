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
            algorithm=DFS(),
            is_perfect=is_perfect
        )
        generator.generate()
        return generator
    return _generate_maze


class TestSolver:
    def test_should_solve_a_perfect_maze(
        self,
        generate_maze: Callable[[int, int, bool], MazeGenerator]
    ):
        generator = generate_maze(10, 10, True)

        solver = Solver(generator.grid, (0, 0), (9, 9))

        assert len(solver.shortest_paths) == 1
        assert len(solver.paths) == 1
        assert solver.paths == solver.shortest_paths
        assert len(solver.wrong_paths) > 0

    def test_should_solve_a_non_perfect_maze(
        self,
        generate_maze: Callable[[int, int, bool], MazeGenerator]
    ):
        generator = generate_maze(10, 10, False)

        solver = Solver(generator.grid, (0, 0), (9, 9))
        min_len = min([len(path) for path in solver.paths])

        assert all([len(path) == min_len for path in solver.shortest_paths])
        assert len(solver.paths) > 1
        assert len(solver.wrong_paths) > 0
