from mazegen.grid import Grid


def test_grid_boundaries() -> None:
    grid = Grid(10, 10)

    # Valid cell retrieval
    assert grid.get_cell(0, 0) is not None
    assert grid.get_cell(9, 9) is not None

    # Out of bounds retrieval must be handled gracefully
    assert grid.get_cell(-1, 5) is None
    assert grid.get_cell(5, 10) is None
