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
from mlx import Mlx
from mlx_api import Image, WallsImage


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
        mlx = Mlx()
        conn = mlx.mlx_init()
        dimensions = mlx.mlx_get_screen_size(conn)
        dimension = min(int(dimensions[1] * 0.8), int(dimensions[2] * 0.8))
        ratio = config.get("WIDTH") / config.get("HEIGHT")
        width = min(int(ratio * dimension), dimension)
        height = int(width / ratio)
        win_ptr = mlx.mlx_new_window(
            conn, width, height, "The Friendly Neighborhood Devs"
        )
        color1 = (255, 43, 55, 132)
        color2 = (255, 177, 19, 19)

        def test(keycode, param):
            print(keycode)
            if keycode == 65307:
                mlx.mlx_loop_exit(conn)
            print(param)
        mlx.mlx_key_hook(win_ptr, test, None)
        walls_image = WallsImage(
            mlx,
            conn,
            generator,
            width,
            height - 20,
            10,
            color1,
            color2,
        )
        background = Image(mlx, conn, width, height)
        for i in range(0, width):
            for j in range(0, height):
                background.put_pixel(i, j, color1)
        white_space = width - walls_image._wall_total * walls_image._maze.grid.width
        margin_left = white_space // 2
        background.render_on_window(win_ptr, 0, 0)
        wall_frames = walls_image.render_frames(win_ptr, (margin_left, 0))

        def frames(_):
            next(wall_frames)
        mlx.mlx_loop_hook(conn, frames, None)

        def close(mlx: Mlx):
            mlx.mlx_loop_exit(conn)
        mlx.mlx_hook(win_ptr, 33, 0, close, mlx)
        mlx.mlx_loop(conn)
        walls_image.destroy()
        mlx.mlx_release(conn)
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
