import sys
from mazegen.grid import Grid
from mazegen.generator import MazeGenerator
from mazegen.algorithms import DFS
from solver import Solver
from maze_config import Config


def main() -> None:
    config: Config
    try:
        config = Config(sys.argv[1])
    except (PermissionError, FileNotFoundError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)

    grid = Grid(config.get("WIDTH"), config.get("HEIGHT"))
    try:
        generator = MazeGenerator(
            grid=grid,
            algorithm=DFS(1),
            is_perfect=config.get("PERFECT"),
            entry_coords=config.get("ENTRY"),
            exit_coords=config.get("EXIT")
        )
        generator.generate()
        solver = Solver(grid, config.get("ENTRY"), config.get("EXIT"))
        with open(config.get("OUTPUT_FILE"), "w") as output_file:
            print(generator.export(), file=output_file)
            print(solver.shortest_paths()[0], file=output_file)
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
