from mazegen.cell import Cell


def test_cell_initialization() -> None:
    cell = Cell(0, 5)
    assert cell.x == 0
    assert cell.y == 5
    assert cell.walls == 15
    assert cell.visited is False


def test_remove_wall() -> None:
    cell = Cell(1, 1)
    # North wall bit is 1. 15 (1111) with North removed becomes 14 (1110)
    cell.remove_wall(1)
    assert cell.has_wall(1) is False
    assert cell.walls == 14
