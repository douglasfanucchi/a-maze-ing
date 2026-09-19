import sys
import random
from typing import Any
from mazegen.grid import Grid
from mazegen.generator import MazeGenerator
from mazegen.algorithms import DepthFirstSearch, HuntAndKill, Kruskal, Prim
from solver import Solver
from maze_config import Config
from mazegen.algorithms import MazeAlgorithm
from mlx import Mlx
from mlx_api import Image, MazeImage


def main() -> None:
    """Execute the maze generation and solving pipeline.

    Reads the configuration file path from command-line arguments, sets the
    global random seed, and initializes the specified generation algorithm.
    It orchestrates the maze generation, solves for the shortest path from
    entry to exit, and writes the hexadecimal representation and solution
    to the configured output file.
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

        # MLX Visualization Pipeline ------------------------------------------
        mlx = Mlx()
        conn = mlx.mlx_init()
        _, screen_width, screen_height = mlx.mlx_get_screen_size(conn)
        safebox_size = min(int(screen_width * 0.8), int(screen_height * 0.8))
        aspect_ratio = config.get("WIDTH") / config.get("HEIGHT")
        window_width = min(int(aspect_ratio * safebox_size), safebox_size)
        window_height = int(window_width / aspect_ratio)
        # Spawn the window slightly taller to absorb the title bar overhead
        win_ptr = mlx.mlx_new_window(
            conn, window_width, window_height, "A-Maze-ing"
        )
        wall_color = (255, 177, 19, 19)
        bg_color = (255, 43, 55, 132)         # Corridor/Interior color
        entry_color = (255, 0, 255, 0)        # Green
        exit_color = (255, 0, 0, 0)           # Black
        pattern_color = (255, 100, 100, 100)  # Gray

        # Initialize and draw the maze onto the off-screen buffer
        maze_image = MazeImage(
            mlx, conn, generator, window_width, window_height, 10.0
        )
        maze_image.draw_maze(
            wall_color,
            bg_color,
            entry_color,
            exit_color,
            pattern_color
        )

        # Calculate centering logic
        maze_pixel_width = maze_image._cell_total * generator.grid.width
        margin_left = (window_width - maze_pixel_width) // 2

        # Prepare the solid window background
        background = Image(mlx, conn, window_width, window_height)
        for i in range(window_width):
            for j in range(window_height):
                background.put_pixel(i, j, bg_color)

        # Define Hooks
        def handle_key(keycode: int, _: Any) -> None:
            # 53 is macOS AppKit ESC, 65307 is Linux/X11 ESC
            if keycode in (53, 65307):
                mlx.mlx_loop_exit(conn)

        def close_window(_: Any) -> None:
            mlx.mlx_loop_exit(conn)

        def render_frame(_: Any) -> None:
            """Push the pre-rendered images to the window every tick."""
            background.render_on_window(win_ptr, 0, 0)
            if maze_image.image is not None:
                maze_image.image.render_on_window(win_ptr, margin_left, 0)

        # Register hooks and execute
        mlx.mlx_key_hook(win_ptr, handle_key, None)
        mlx.mlx_hook(win_ptr, 33, 0, close_window, None)  # 33 is DestroyNotify
        mlx.mlx_loop_hook(conn, render_frame, None)
        mlx.mlx_loop(conn)

        # Safe memory cleanup
        mlx.mlx_destroy_window(conn, win_ptr)
        maze_image.destroy()
        background.destroy()
        if hasattr(mlx, 'mlx_release'):
            mlx.mlx_release(conn)
    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
