import sys
import random
from mazegen.grid import Grid
from mazegen.generator import MazeGenerator
from mazegen.algorithms import DFS
from solver import Solver
from maze_config import Config
from mazegen.algorithms import MazeAlgorithm


def main() -> None:
    if len(sys.argv) < 2:
        sys.stderr.write("Error: Too few arguments\n")
        sys.exit(1)
    try:
        config = Config(sys.argv[1])
    except (PermissionError, FileNotFoundError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

    random.seed(config.get("SEED"))
    grid = Grid(config.get("WIDTH"), config.get("HEIGHT"))
    algorithms: dict[str, MazeAlgorithm] = {
        "DFS": DFS(),
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
            print(solver.shortest_paths[0], file=output_file)
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
