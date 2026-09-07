import pytest
from mazegen.cell import Cell
from mazegen.direction import Direction


class TestCell:
    def test_should_create_basic_cell(self):
        cell = Cell(3, 7)

        assert cell.x == 3
        assert cell.y == 7
        assert cell.has_wall(Direction.NORTH)
        assert cell.has_wall(Direction.EAST)
        assert cell.has_wall(Direction.SOUTH)
        assert cell.has_wall(Direction.WEST)
        assert cell.visited is False

    @pytest.mark.parametrize("x, y", [(-1, 0), (0, -1), (-1, -1)])
    def test_should_not_create_cell_with_invalid_coordinates(self, x, y):
        with pytest.raises(ValueError):
            Cell(x, y)

    @pytest.mark.parametrize(
        "direction, expected_bitmask",
        [
            (Direction.NORTH, 14), 
            (Direction.EAST, 13),  
            (Direction.SOUTH, 11), 
            (Direction.WEST, 7),   
        ],
    )
    def test_should_remove_wall_and_update_bitmask(self, direction: Direction, expected_bitmask: int) -> None:
        cell = Cell(5, 5)
        cell.remove_wall(direction)
        assert cell.has_wall(direction) is False
        assert cell.walls == expected_bitmask

    @pytest.mark.parametrize(
        "broken_sides, expected_hex",
        [
            ([Direction.WEST, Direction.SOUTH, Direction.EAST], "1"),
            ([Direction.WEST, Direction.SOUTH], "3"),
            ([Direction.WEST], "7"),
            ([], "f"),
        ],
    )
    def test_should_check_hex_representation_of_broken_walls(
        self, broken_sides: list[Direction], expected_hex: str
    ) -> None:
        cell = Cell(2, 3)
        for side in broken_sides:
            cell.remove_wall(side)
        assert cell.to_hex() == expected_hex

    @pytest.mark.parametrize(
        "walls,expected",
        [
            (Direction.NORTH + Direction.EAST + Direction.SOUTH + Direction.WEST, 4),
            (Direction.NORTH + Direction.EAST + Direction.SOUTH, 3),
            (Direction.NORTH + Direction.EAST, 2),
            (Direction.NORTH, 1),
        ]
    )
    def test_should_count_amount_of_walls(
        self,
        walls: int,
        expected: int
    ):
        cell = Cell(0, 0)
        cell.walls = walls
        assert cell.count_walls() == expected
