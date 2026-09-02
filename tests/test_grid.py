import pytest
from mazegen.cell import Cell
from mazegen.grid import Grid
from mazegen.direction import Direction


class TestGrid:
    def test_should_initialize_grid_dimensions_and_matrix(self) -> None:
        grid = Grid(3, 4)

        assert grid.width == 3
        assert grid.height == 4
        assert len(grid.matrix) == 4  # 4 rows (y)
        assert len(grid.matrix[0]) == 3  # 3 columns (x)
        
        # Verify specific cell coordinates
        assert grid.matrix[2][1].x == 1
        assert grid.matrix[2][1].y == 2
        assert isinstance(grid.matrix[0][0], Cell)

    @pytest.mark.parametrize("width, height", [(-1, 5), (5, -1), (0, 5), (5, 0)])
    def test_should_reject_invalid_grid_dimensions(self, width: int, height: int) -> None:
        with pytest.raises(ValueError):
            Grid(width, height)

    @pytest.mark.parametrize(
        "x, y",
        [
            (-1, 2),  # Negative x
            (2, -1),  # Negative y
            (5, 2),   # x out of bounds (width is 5, max index is 4)
            (2, 5),   # y out of bounds (height is 5, max index is 4)
        ],
    )
    def test_should_return_none_for_out_of_bounds_cells(self, x: int, y: int) -> None:
        grid = Grid(5, 5)
        assert grid.get_cell(x, y) is None

    def test_should_return_correct_cell_within_bounds(self) -> None:
        grid = Grid(5, 5)
        cell = grid.get_cell(2, 3)

        assert cell is not None
        assert cell.x == 2
        assert cell.y == 3

    def test_should_get_all_unvisited_neighbors_for_center_cell(self) -> None:
        grid = Grid(3, 3)
        center_cell = grid.get_cell(1, 1)
        assert center_cell is not None

        neighbors = grid.get_unvisited_neighbors(center_cell)
        
        assert len(neighbors) == 4
        
        # Verify the returned structure is list[tuple[Direction, Cell]]
        directions = [n[0] for n in neighbors]
        assert Direction.NORTH in directions
        assert Direction.EAST in directions
        assert Direction.SOUTH in directions
        assert Direction.WEST in directions

    def test_should_ignore_out_of_bounds_and_visited_neighbors(self) -> None:
        grid = Grid(3, 3)
        corner_cell = grid.get_cell(0, 0)
        assert corner_cell is not None

        # Manually mark the East neighbor as visited
        east_neighbor = grid.get_cell(1, 0)
        assert east_neighbor is not None
        east_neighbor.visited = True

        neighbors = grid.get_unvisited_neighbors(corner_cell)
        
        # Corner cell normally has 2 neighbors (East, South)
        # Since East is visited, only South should remain.
        assert len(neighbors) == 1
        assert neighbors[0][0] == Direction.SOUTH
        assert neighbors[0][1].x == 0
        assert neighbors[0][1].y == 1
