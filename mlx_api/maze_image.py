"""Module for rendering a maze grid onto an MLX image canvas."""

from mlx import Mlx
from mazegen import MazeGenerator
from typing import Any, Optional
from mlx_api import Image
from mazegen.cell import Cell
from mazegen.direction import Direction


class MazeImage:
    """Wrapper for building and drawing maze representation onto an MLX image.

    Translates grid cell states and wall bitmasks into pixel coordinates,
    handling interior backgrounds, wall segments, corner joints, and special
    markers (entry, exit, 42 pattern).
    """

    def __init__(
        self,
        mlx: Mlx,
        mlx_conn: Any,
        maze: MazeGenerator,
        width: int,
        height: int,
        wall_thickness: float
    ) -> None:
        """Initialize the maze image layout parameters and buffer.

        Args:
            mlx: The Mlx instance wrapping the underlying graphical library.
            mlx_conn: The MLX connection identifier.
            maze: The MazeGenerator instance containing grid data.
            width: Total image width in pixels.
            height: Total image height in pixels.
            wall_thickness: Percentage (0-100) of cell size reserved for walls.
        """
        self._maze = maze
        self._wall_total = min(
            width // maze.grid.width,
            height // maze.grid.height
        )
        self._image = Image(mlx, mlx_conn, width, height)
        self._wall_thickness = max(
            1,
            int(self._wall_total * wall_thickness) // 100
        )
        self._wall_len = max(1, self._wall_total - (self._wall_thickness * 2))

    @property
    def image(self) -> Optional[Image]:
        """Return the underlying MLX Image canvas.

        Returns:
            The instantiated Image wrapper or None if destroyed.
        """
        return self._image

    def destroy(self) -> None:
        """Release the underlying image pixel buffer."""
        if self.image is not None:
            self.image.destroy()

    def _paint_wall(
        self,
        coord: tuple[int, int],
        direction: Direction,
        color: tuple[int, int, int, int]
    ) -> None:
        x = coord[0] * self._wall_total
        y = coord[1] * self._wall_total
        if direction == Direction.NORTH or direction == Direction.SOUTH:
            x += self._wall_thickness
            if direction == Direction.SOUTH:
                y += self._wall_thickness + self._wall_len
            for i in range(0, self._wall_len):
                for j in range(0, self._wall_thickness):
                    self._image.put_pixel(x + i, y + j, color)
            return
        y += self._wall_thickness
        if direction == Direction.EAST:
            x += self._wall_len + self._wall_thickness
        for i in range(0, self._wall_thickness):
            for j in range(0, self._wall_len):
                self._image.put_pixel(x + i, y + j, color)

    def _paint_corners(
        self,
        coord: tuple[int, int],
        vector: tuple[int, int],
        color: tuple[int, int, int, int]
    ) -> None:
        x = (
            coord[0] * self._wall_total
            + vector[0] * (self._wall_len + self._wall_thickness)
        )
        y = (
            coord[1] * self._wall_total
            + vector[1] * (self._wall_len + self._wall_thickness)
        )
        for i in range(0, self._wall_thickness):
            for j in range(0, self._wall_thickness):
                self._image.put_pixel(x + i, y + j, color)

    def _paint_cell_background(
        self,
        cell: Cell,
        color: tuple[int, int, int, int]
    ) -> None:
        for i in range(0, self._wall_len):
            for j in range(0, self._wall_len):
                self._image.put_pixel(
                    cell.x * self._wall_total + self._wall_thickness + i,
                    cell.y * self._wall_total + self._wall_thickness + j,
                    color
                )
