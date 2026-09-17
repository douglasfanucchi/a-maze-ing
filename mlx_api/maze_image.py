from mlx import Mlx
from mazegen import MazeGenerator
from typing import Any
from mlx_api import Image
from mazegen.cell import Cell
from mazegen.direction import Direction
from typing import Callable, Optional


class MazeImage:
    def __init__(
        self,
        mlx: Mlx,
        mlx_conn: Any,
        maze: MazeGenerator,
        width: int,
        height: int,
        background_color: tuple[int, int, int, int],
        wall_color: tuple[int, int, int, int]
    ):
        self._conn = mlx_conn
        self._maze = maze
        self._legend_height = 0
        self._wall_total = min(
            width // maze.grid.width,
            height // maze.grid.height
        )
        self._image = Image(mlx, mlx_conn, width, height)
        thickness_percentage = 10
        self._wall_thickness = max(
            1,
            (self._wall_total * thickness_percentage) // 100
        )
        self._mlx = mlx
        self._wall_color = wall_color
        self._background_color = background_color
        self._wall_len = self._wall_total - self._wall_thickness * 2

    def destroy(self) -> None:
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
        color: tuple[int, int, int, int]) -> None:
            x = (coord[0] * self._wall_total
                    + vector[0] * (self._wall_len + self._wall_thickness)
                )
            y = (coord[1] * self._wall_total
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

    @property
    def image(self) -> Optional[Image]:
        return self._image
