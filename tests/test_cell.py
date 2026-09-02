import pytest

from mazegen.cell import Cell
from mazegen.direction import Direction


class TestCell:
    def test_should_create_basic_cell(self):
        cell = Cell(3, 7)

        assert cell.get_x() == 3
        assert cell.get_y() == 7
        assert cell.has_wall("N")
        assert cell.has_wall("E")
        assert cell.has_wall("S")
        assert cell.has_wall("W")
        assert cell.is_visited() is False

    @pytest.mark.parametrize("x, y", [(-1, 0), (0, -1), (-1, -1)])
    def test_should_not_create_cell_with_invalid_coordinates(self, x, y):
        with pytest.raises(ValueError):
            Cell(x, y)

    @pytest.mark.parametrize("side", ["N", "E", "S", "W"])
    def test_should_break_wall_of_a_cell(self, side):
        cell = Cell(5, 5)

        cell.break_wall(side)

        assert cell._walls[side] is False

    @pytest.mark.parametrize("side", ["N", "E", "S", "W"])
    def test_should_check_for_non_existing_wall(self, side):
        cell = Cell(5, 5)

        cell.break_wall(side)

        assert cell.has_wall(side) is False

    @pytest.mark.parametrize(
        "side, direction, expected_bitmask",
        [
            ("N", Direction.NORTH, 0b1110),
            ("E", Direction.EAST, 0b1101),
            ("S", Direction.SOUTH, 0b1011),
            ("W", Direction.WEST, 0b0111),
        ],
    )
    def test_should_check_bitmask_values_of_broken_walls(
        self, side, direction, expected_bitmask
    ):
        cell = Cell(5, 5)

        cell._walls[side] = False

        assert cell.to_bitmask() == expected_bitmask
        assert cell.to_bitmask() & direction == 0

    @pytest.mark.parametrize(
        "broken_sides, expected_hex",
        [
            (["W", "S", "E"], "1"),
            (["W", "S"], "3"),
            (["W"], "7"),
            ([], "f"),
        ],
    )
    def test_should_check_hex_representation_of_broken_walls(
        self, broken_sides, expected_hex
    ):
        cell = Cell(2, 3)

        for side in broken_sides:
            cell._walls[side] = False

        assert cell.to_hex() == expected_hex
