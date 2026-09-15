import sys
import random
from mazegen.grid import Grid
from mazegen.generator import MazeGenerator
from mazegen.algorithms import DepthFirstSearch
from mazegen.algorithms import HuntAndKill
from mazegen.algorithms import Kruskal
from mazegen.algorithms import Prim
from solver import Solver
from maze_config import Config
from mazegen.algorithms import MazeAlgorithm


def main() -> None:
    """Execute the maze generation and solving pipeline.

    Reads the configuration file path from command-line arguments, sets the
    global random seed, and initializes the specified generation algorithm.
    It orchestrates the maze generation, solves for the shortest path from
    entry to exit, and writes the hexadecimal representation and solution
    to the configured output file.

    File access issues, invalid configurations, or generation constraint
    violations (such as grid size) are caught, printed to standard error,
    and result in a non-zero system exit.
    """
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 a_maze_ing.py config.txt\n")
        sys.exit(1)
    try:
        config = Config(sys.argv[1])
    except (PermissionError, FileNotFoundError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

    random.seed(config.get("SEED"))
    grid = Grid(config.get("WIDTH"), config.get("HEIGHT"))
    algorithms: dict[str, MazeAlgorithm] = {
        "DFS": DepthFirstSearch(),
        "Kruskal": Kruskal(),
        "HuntAndKill": HuntAndKill(),
        "Prim": Prim(),
    }
    algorithm: str = config.get("ALGORITHM")
    try:
        generator = MazeGenerator(
            grid=grid,
            algorithm=algorithms[algorithm],
            is_perfect=config.get("PERFECT"),
            entry_coords=config.get("ENTRY"),
            exit_coords=config.get("EXIT")
        )
        generator.generate()
        solver = Solver(grid, config.get("ENTRY"), config.get("EXIT"))
        with open(config.get("OUTPUT_FILE"), "w") as output_file:
            print(generator.export(), file=output_file)
            print(solver.shortest_path, file=output_file)
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
