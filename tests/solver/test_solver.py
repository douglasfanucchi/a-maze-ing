import unittest
from mazegen.grid import Grid
from mazegen.direction import Direction
from solver import Solver


class TestSolver(unittest.TestCase):
    """Test suite for the BFS shortest path Solver."""

    def setUp(self) -> None:
        """Initialize a fresh 3x3 grid before each test."""
        self.grid = Grid(3, 3)

    def test_straight_path(self) -> None:
        """Test finding a direct path across a single corridor."""
        # Carve a horizontal corridor: (0,0) -> (1,0) -> (2,0)
        c00 = self.grid.get_cell(0, 0)
        c10 = self.grid.get_cell(1, 0)
        c20 = self.grid.get_cell(2, 0)
        self.grid.connect_cells(c00, c10, Direction.EAST)
        self.grid.connect_cells(c10, c20, Direction.EAST)

        solver = Solver(self.grid, (0, 0), (2, 0))
        self.assertEqual(solver.shortest_path, "EE")

    def test_unreachable_exit(self) -> None:
        """Test behavior when no valid path exists to the exit."""
        # Grid is fully walled off by default
        solver = Solver(self.grid, (0, 0), (2, 2))
        self.assertEqual(solver.shortest_path, "")

    def test_start_equals_exit(self) -> None:
        """Test behavior when the entry and exit are the exact same cell."""
        # A path of zero steps should result in an empty string
        solver = Solver(self.grid, (1, 1), (1, 1))
        self.assertEqual(solver.shortest_path, "")

    def test_out_of_bounds_entry(self) -> None:
        """Test safety guard when entry coordinates do not exist."""
        solver = Solver(self.grid, (-1, -1), (0, 0))
        self.assertEqual(solver.shortest_path, "")

    def test_complex_winding_path(self) -> None:
        """Test a winding U-shaped path to ensure correct backtracking."""
        # Carve a U-shape:
        # (0,0) -> (1,0) -> (2,0)
        #                    |
        # (0,1) <- (1,1) <- (2,1)
        
        cells = {
            "00": self.grid.get_cell(0, 0),
            "10": self.grid.get_cell(1, 0),
            "20": self.grid.get_cell(2, 0),
            "21": self.grid.get_cell(2, 1),
            "11": self.grid.get_cell(1, 1),
            "01": self.grid.get_cell(0, 1),
        }
        
        self.grid.connect_cells(cells["00"], cells["10"], Direction.EAST)
        self.grid.connect_cells(cells["10"], cells["20"], Direction.EAST)
        self.grid.connect_cells(cells["20"], cells["21"], Direction.SOUTH)
        self.grid.connect_cells(cells["21"], cells["11"], Direction.WEST)
        self.grid.connect_cells(cells["11"], cells["01"], Direction.WEST)

        solver = Solver(self.grid, (0, 0), (0, 1))
        # Steps should be East, East, South, West, West
        self.assertEqual(solver.shortest_path, "EESWW")

    def test_shortest_path_over_loop(self) -> None:
        """Test BFS mathematically guarantees the shortest path in a loop."""
        # Create a loop where (0,0) connects to (1,1) via two paths:
        # Path A (Fast): (0,0) -> (1,0) -> (1,1)
        # Path B (Slow): (0,0) -> (0,1) -> (0,2) -> (1,2) -> (1,1)
        
        c00, c10, c11 = [self.grid.get_cell(x, y) for x, y in [(0, 0), (1, 0), (1, 1)]]
        c01, c02, c12 = [self.grid.get_cell(x, y) for x, y in [(0, 1), (0, 2), (1, 2)]]
        
        # Fast path
        self.grid.connect_cells(c00, c10, Direction.EAST)
        self.grid.connect_cells(c10, c11, Direction.SOUTH)
        
        # Slow path
        self.grid.connect_cells(c00, c01, Direction.SOUTH)
        self.grid.connect_cells(c01, c02, Direction.SOUTH)
        self.grid.connect_cells(c02, c12, Direction.EAST)
        self.grid.connect_cells(c12, c11, Direction.NORTH)

        solver = Solver(self.grid, (0, 0), (1, 1))
        
        # Because it's a loop, it could be ES or SE depending on direction
        # enum order, but its length MUST be exactly 2.
        self.assertEqual(len(solver.shortest_path), 2)
        self.assertIn(solver.shortest_path, ["ES", "SE"])


if __name__ == "__main__":
    unittest.main()
