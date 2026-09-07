from mazegen.algorithms import DFS
from mazegen.grid import Grid
from mazegen.direction import Direction

class TestDFS:
    def test_should_connect_cells_on_a_2x2_grid(self):
        grid = Grid(2, 2)
        algo = DFS(1)
        algo.execute(grid)

        assert grid.get_cell(0, 0).has_wall(Direction.NORTH)
        assert not grid.get_cell(0, 0).has_wall(Direction.EAST)
        assert grid.get_cell(0, 0).has_wall(Direction.WEST)
        assert grid.get_cell(0, 0).has_wall(Direction.SOUTH)

        assert grid.get_cell(1, 0).has_wall(Direction.NORTH)
        assert grid.get_cell(1, 0).has_wall(Direction.EAST)
        assert not grid.get_cell(1, 0).has_wall(Direction.SOUTH)
        assert not grid.get_cell(1, 0).has_wall(Direction.WEST)

        assert not grid.get_cell(1, 1).has_wall(Direction.NORTH)
        assert grid.get_cell(1, 1).has_wall(Direction.EAST)
        assert grid.get_cell(1, 1).has_wall(Direction.SOUTH)
        assert not grid.get_cell(1, 1).has_wall(Direction.WEST)

        assert grid.get_cell(0, 1).has_wall(Direction.NORTH)
        assert not grid.get_cell(0, 1).has_wall(Direction.EAST)
        assert grid.get_cell(0, 1).has_wall(Direction.WEST)
        assert grid.get_cell(0, 1).has_wall(Direction.SOUTH)
