import sys
import random
from typing import Any
from mazegen import MazeGenerator
from maze_config import Config
from mlx import Mlx  # type: ignore[import-untyped, unused-ignore]
from mlx_api import Image, MazeImage, PathImage


def get_generator(config: Config) -> MazeGenerator:
    """Initialize the grid and maze generator from the given configuration.

    Args:
        config (Config): The configuration object containing
        the maze dimensions, algorithm choice, perfect/imperfect flag
        and start/exit coordinates.

    Returns:
        tuple[Grid, MazeGenerator]: A tuple containing the newly created empty
        grid and the configured maze generator ready to carve it.

    Raises:
        ValueError: If the entry or exit coordinates are invalid or fall
        outside the grid boundaries.
    """
    generator = MazeGenerator(
        config.get("WIDTH"),
        config.get("HEIGHT"),
        algorithm=config.get("ALGORITHM"),
        is_perfect=config.get("PERFECT"),
        entry_coords=config.get("ENTRY"),
        exit_coords=config.get("EXIT")
    )
    return generator


def handle_key(keycode: int, context: dict[str, Any]) -> None:
    """Handle keyboard interactions and runtime maze regeneration.

    Listens for specific keystrokes to either close the MLX window gracefully
    (ESC) or dynamically generate, solve, and render a brand-new maze ('1').
    It manages memory safely by destroying old image buffers before rendering
    the new state.

    Args:
        keycode (int): The hardware-specific integer code of the key pressed.
        context (dict[str, Any]): The shared mutable state dictionary
        containing MLX connection pointers, color profiles, configuration data
        and the active image objects.
    """
    mlx = context["mlx"]
    conn = context["conn"]

    # 18 is macOS AppKit '1', 49 is Linux/X11 ASCII '1'
    if keycode in (18, 49):
        config = context["config"]
        try:
            new_generator = get_generator(config)
            new_generator.generate()
        except ValueError as e:
            print(f"Regeneration failed: {e}")
            return
        context["generator"] = new_generator
        context["shortest_path"] = new_generator.shortest_path_cells
        # Destroy old buffers to prevent memory leaks
        context["path_image"].destroy()
        context["maze_image"].destroy()
        # Rebuild visual assets and store them back in the context dictionary
        context["maze_image"] = MazeImage(
            mlx,
            conn,
            new_generator,
            context["window_width"],
            context["window_height"],
            10.0
        )
        context["maze_image"].draw_maze(
            context["wall_color"],
            context["bg_color"],
            context["entry_color"],
            context["exit_color"],
            context["pattern_color"]
        )
        context["path_image"] = PathImage(
            mlx,
            conn,
            new_generator,
            context["window_width"],
            context["window_height"],
            10.0,
            context["path_color"],
            new_generator.shortest_path_cells
        )
        # Reset the animation frame generator
        context["path_frames"] = context["path_image"].render_frames(
            context["win_ptr"],
            (context["padding_left"], context["padding_top"])
        )

    # 19 is macOS AppKit '2', 50 is Linux/X11 ASCII '2'
    elif keycode in (19, 50):
        context["show_path"] = not context["show_path"]

    # 20 is macOS AppKit '3', 51 is Linux/X11 ASCII '3'
    elif keycode in (20, 51):
        # Shift the palette index and update current colors
        num_colors = len(context["palettes"])
        context["palette_idx"] = (context["palette_idx"] + 1) % num_colors
        new_palette = context["palettes"][context["palette_idx"]]

        context["wall_color"] = new_palette["wall"]
        context["bg_color"] = new_palette["bg"]
        context["entry_color"] = new_palette["entry"]
        context["exit_color"] = new_palette["exit"]
        context["pattern_color"] = new_palette["pattern"]
        context["path_color"] = new_palette["path"]

        # Destroy old buffers
        context["path_image"].destroy()
        context["maze_image"].destroy()
        context["background"].destroy()

        # Rebuild background
        new_bg = Image(
            mlx, conn, context["window_width"], context["total_window_height"]
            )
        for i in range(context["window_width"]):
            for j in range(context["total_window_height"]):
                new_bg.put_pixel(i, j, context["bg_color"])
        context["background"] = new_bg

        # Redraw maze using the existing generator from context
        context["maze_image"] = MazeImage(
            mlx,
            conn,
            context["generator"],
            context["window_width"],
            context["window_height"],
            wall_thickness=10.0
        )
        context["maze_image"].draw_maze(
            context["wall_color"], context["bg_color"], context["entry_color"],
            context["exit_color"], context["pattern_color"]
        )

        # Redraw path using the existing path from context
        context["path_image"] = PathImage(
            mlx,
            conn,
            context["generator"],
            context["window_width"],
            context["window_height"],
            wall_thickness=10.0,
            color=context["path_color"],
            shortest_path=context["shortest_path"]
        )
        context["path_frames"] = context["path_image"].render_frames(
            context["win_ptr"],
            (context["padding_left"], context["padding_top"])
        )

    # 53 is macOS AppKit ESC, 65307 is Linux/X11 ESC
    # 21 is macOS AppKit '4', 51 is Linux/X11 ASCII '4'
    elif keycode in (53, 65307, 21, 52):
        mlx.mlx_loop_exit(conn)


def visualization_pipeline(config: Config, generator: MazeGenerator) -> None:
    """Execute the MLX graphical rendering and interactive event loop.

    Sets up the MLX window dimensions, draws the static maze layout to an
    off-screen buffer, and initializes the pathfinding animation. It packs the
    runtime state into a context dictionary for the event hooks and launches
    the infinite rendering loop.

    Args:
        config (Config): The configuration object defining the maze dimensions
            and logic parameters.
        generator (MazeGenerator): The generator holding the fully carved grid
            structure.
    """
    mlx = Mlx()
    conn = mlx.mlx_init()
    if conn is None:
        sys.stderr.write(
            "Error: Couldn't establish a connection "
            "with the graphical server"
        )
        sys.exit(1)
    _, screen_width, screen_height = mlx.mlx_get_screen_size(conn)
    safebox_size = min(int(screen_width * 0.8), int(screen_height * 0.8))
    aspect_ratio = config.get("WIDTH") / config.get("HEIGHT")
    pre_window_width = min(int(aspect_ratio * safebox_size), safebox_size)
    window_height = int(pre_window_width / aspect_ratio)
    # Ensure minimum width for legend
    window_width = max(pre_window_width, 475)
    footer_height = 40
    total_window_height = window_height + footer_height
    win_ptr = mlx.mlx_new_window(
        conn, window_width, total_window_height, "A-Maze-ing"
    )
    palettes = [
        {
            "wall": (255, 23, 0, 255),
            "bg": (255, 0, 0, 0),
            "entry": (255, 255, 255, 11),
            "exit": (255, 251, 0, 7),
            "pattern": (255, 255, 255, 255),
            "path": (255, 255, 255, 11),
        },
        {
            "wall": (255, 177, 19, 19),
            "bg": (255, 43, 55, 132),
            "entry": (255, 255, 255, 255),
            "exit": (255, 0, 0, 0),
            "pattern": (255, 100, 100, 100),
            "path": (255, 255, 255, 255),
        },
        {
            "wall": (255, 63, 216, 71),
            "bg": (255, 5, 5, 5),
            "entry": (255, 255, 234, 4),
            "exit": (255, 232, 0, 13),
            "pattern": (255, 233, 86, 38),
            "path": (255, 255, 234, 4),
        },
    ]

    # Prepare the solid window background
    background = Image(mlx, conn, window_width, total_window_height)
    for i in range(window_width):
        for j in range(total_window_height):
            background.put_pixel(i, j, palettes[0]["bg"])
    endian = background._endian

    # Initialize and draw the maze onto the off-screen buffer
    maze_image = MazeImage(
        mlx, conn, generator, window_width, window_height, 10.0
    )
    maze_image.draw_maze(
        wall_color=palettes[0]["wall"],
        bg_color=palettes[0]["bg"],
        entry_color=palettes[0]["entry"],
        exit_color=palettes[0]["exit"],
        pattern_color=palettes[0]["pattern"]
    )

    # Calculate centering logic
    maze_pixel_width = (
        maze_image._cell_total * generator.grid.width
        + maze_image._wall_thickness * 2
    )
    maze_pixel_height = (
        maze_image._cell_total * generator.grid.height
        + maze_image._wall_thickness * 2
    )
    padding_left = (window_width - maze_pixel_width) // 2
    padding_top = (window_height - maze_pixel_height) // 2

    # Initialize the PathImage with the shortest path
    path_color = palettes[0]["path"]
    path_image = PathImage(
        mlx,
        conn,
        generator,
        window_width,
        window_height,
        10.0,
        path_color,
        generator.shortest_path_cells
    )

    # Initialize the generator passing the exact same offset as the maze
    path_frames = path_image.render_frames(
        win_ptr, (padding_left, padding_top)
    )

    # Pack the mutable state into a dictionary
    context: dict[str, Any] = {
            "mlx": mlx,
            "conn": conn,
            "win_ptr": win_ptr,
            "config": config,
            "generator": generator,
            "shortest_path": generator.shortest_path_cells,
            "window_width": window_width,
            "window_height": window_height,
            "total_window_height": total_window_height,
            "padding_left": padding_left,
            "padding_top": padding_top,
            "endian": endian,
            "palettes": palettes,
            "palette_idx": 0,
            "background": background,
            "wall_color": palettes[0]["wall"],
            "bg_color": palettes[0]["bg"],
            "entry_color": palettes[0]["entry"],
            "exit_color": palettes[0]["exit"],
            "pattern_color": palettes[0]["pattern"],
            "path_color": palettes[0]["path"],
            "maze_image": maze_image,
            "path_image": path_image,
            "path_frames": path_frames,
            "show_path": True,
        }

    def close_window(_: Any) -> None:
        mlx.mlx_loop_exit(conn)

    def render_frame(_: Any) -> None:
        """Push the pre-rendered images to the window every tick."""
        context["background"].render_on_window(win_ptr, 0, 0)
        current_maze = context["maze_image"]
        if current_maze.image is not None:
            current_maze.image.render_on_window(
                win_ptr, padding_left, padding_top
            )
        if context["show_path"]:
            next(context["path_frames"])
        # Convert tuple (A, R, G, B) to 32-bit integer
        _, r, g, b = context["wall_color"]
        if context["endian"] == 0:
            text_color = (b << 16) | (g << 8) | r
        else:
            text_color = (r << 16) | (g << 8) | b
        # Position the text inside the footer area
        x_pos = 25
        y_pos = context["total_window_height"] - 25
        legend = "1: regen    2: path    3: color    4: quit"
        context["mlx"].mlx_string_put(
            context["conn"], context["win_ptr"],
            x_pos, y_pos, text_color, legend
        )

    # Register hooks and execute
    mlx.mlx_key_hook(win_ptr, handle_key, context)
    mlx.mlx_hook(win_ptr, 33, 0, close_window, None)  # 33 is DestroyNotify
    mlx.mlx_loop_hook(conn, render_frame, context)
    mlx.mlx_loop(conn)

    # Clean up memory using the final dictionary states
    mlx.mlx_destroy_window(conn, win_ptr)
    context["path_image"].destroy()
    context["maze_image"].destroy()
    context["background"].destroy()
    if hasattr(mlx, 'mlx_release'):
        mlx.mlx_release(conn)


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
    try:
        generator = get_generator(config)
        generator.generate()
        with open(config.get("OUTPUT_FILE"), "w") as output_file:
            print(generator.export(), file=output_file)
            print(generator.shortest_path, file=output_file)
        visualization_pipeline(config, generator)
    except (ValueError, OSError) as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
