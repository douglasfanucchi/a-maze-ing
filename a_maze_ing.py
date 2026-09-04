import sys
from mazegen.grid import Grid
from mazegen.generator import MazeGenerator
from mazegen.algorithms import MazeAlgorithm


def main() -> None:
    # Parse and validate config.txt initializing variables:
    # width, height, algorithm (default DFS),
    # is_perfect (Default False), entry_coords and exit_coords

    # Placeholder values:
    width: int = 20
    height: int = 20
    is_perfect: bool = False
    algorithm: MazeAlgorithm
    entry_coords = (0, 0)
    exit_coords = (width - 1, height - 1)
    # --------------------------------------------

    grid = Grid(width, height)
    try:
        generator = MazeGenerator(
            grid=grid,
            algorithm=algorithm,
            is_perfect=is_perfect,
            entry_coords=entry_coords,
            exit_coords=exit_coords
        )
        generator.generate()
        print(generator.export())
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
