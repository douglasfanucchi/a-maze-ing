"""Module for animating the shortest path solution on an MLX image canvas."""

from typing import Any, Generator
from mazegen.cell import Cell
from mazegen import MazeGenerator
from .maze_image import MazeImage


class PathImage(MazeImage):
    """Animate the solver's shortest path over a maze.

    Draws on its own transparent image, meant to be layered on top of the
    walls image. The shortest path is painted cell by cell, joining each
    to the next by a rectangle inset from the walls.

    Attributes:
        _color (tuple[int, int, int, int]): ARGB color used to draw the path.
        _shortest_path (list[Cell]): Sequence of cells forming the path.
        _padding (int): Visual inset padding in pixels for path rectangles.
    """

    def __init__(
        self,
        mlx: Any,
        mlx_conn: Any,
        maze: MazeGenerator,
        width: int,
        height: int,
        wall_thickness: float,
        color: tuple[int, int, int, int],
        shortest_path: list[Cell]
    ) -> None:
        """Create the image and store the path data the animation needs.

        Args:
            mlx (Any): The Mlx instance wrapping the loaded MLX library.
            mlx_conn (Any): The MLX connection identifier returned by mlx_init.
            maze (MazeGenerator): The generated maze the path belongs to.
            width (int): The width of the image canvas in pixels.
            height (int): The height of the image canvas in pixels.
            wall_thickness (float): Wall thickness as percentage of cell size.
            color (tuple[int, int, int, int]): ARGB color to paint the path.
            shortest_path (list[Cell]): Cells sequence representing the path.

        Raises:
            Exception: If MLX fails to allocate the underlying image buffer.
        """
        super().__init__(mlx, mlx_conn, maze, width, height, wall_thickness)
        self._color = color
        self._shortest_path = shortest_path
        self._padding = int(0.40 * self._cell_interior)

    def render_frames(
        self,
        win_ptr: Any,
        coords: tuple[int, int]
    ) -> Generator[None, None, None]:
        """Draw the animation one frame per step.

        Each cell of the shortest path is one frame. Once the animation ends,
        the generator yields infinitely to keep the final state on screen.
        """
        for index, cell in enumerate(self._shortest_path):
            if index < len(self._shortest_path) - 1:
                self._connect_cells(
                    cell,
                    self._shortest_path[index + 1],
                    self._color
                )
            # Push the updated buffer to the window
            if self._image is not None:
                self._image.render_on_window(win_ptr, *coords)
            yield
        # Keep pushing the finished image to the window after animation ends
        while True:
            if self._image is not None:
                self._image.render_on_window(win_ptr, *coords)
            yield

    def _connect_cells(
        self,
        v: Cell,
        w: Cell,
        color: tuple[int, int, int, int]
    ) -> None:
        """Paint a rectangle joining the centers of two adjacent cells."""
        padding = min(self._padding, (self._cell_interior - 1) // 2)
        thickness = self._cell_interior - (padding * 2)
        # Add self._offset to align perfectly with the framed maze coordinates
        cell_offset = 2 * self._wall_thickness + padding
        v_x = v.x * self._cell_total + cell_offset
        v_y = v.y * self._cell_total + cell_offset
        w_x = w.x * self._cell_total + cell_offset
        w_y = w.y * self._cell_total + cell_offset
        start_x = min(v_x, w_x)
        start_y = min(v_y, w_y)
        # Determine dimensions based on whether
        # the segment is horizontal or vertical
        rect_w = abs(w_x - v_x) + thickness
        rect_h = abs(w_y - v_y) + thickness
        self._fill_rect(start_x, start_y, rect_w, rect_h, color)
