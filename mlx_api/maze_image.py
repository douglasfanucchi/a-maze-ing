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
        thickness_percentage = 1
        self._wall_thickness = max(
            1,
            (self._wall_total * thickness_percentage) // 100
        )
        self._wall_length = self._wall_total - self._wall_thickness * 2
        self._mlx = mlx
        self._wall_color = wall_color
        self._draw_map: dict[
            Direction,
            Callable[[Cell, tuple[int, int, int, int]], None]
        ] = {
            Direction.NORTH: self._draw_top_wall,
            Direction.EAST: self._draw_right_wall,
            Direction.SOUTH: self._draw_bottom_wall,
            Direction.WEST: self._draw_left_wall,
        }
        self._background_color = background_color

    def create(self) -> None:
        for row in self._maze.grid.matrix:
            for cell in row:
                self._paint_cell_background(cell)
                for direction in Direction:
                    if cell.has_wall(direction):
                        self.draw_wall(cell, direction, self._wall_color)

    def render(self, win_ptr: Any, win_width: int) -> None:
        white_space = win_width - self._wall_total * self._maze.grid.width
        margin_left = white_space // 2
        self._image.render_on_window(win_ptr, margin_left, 0)

    def draw_wall(
        self,
        cell: Cell,
        direction: Direction,
        argb: tuple[int, int, int, int]
    ):
        return self._draw_map[direction](cell, argb)

    def _draw_top_wall(
        self,
        cell: Cell,
        argb: tuple[int, int, int, int],
    ) -> None:
        extend_wall = 0
        if not cell.has_wall(Direction.EAST):
            extend_wall = 1
        self._draw_wall(
            (cell.x * self._wall_total, cell.y * self._wall_total),
            self._wall_total + extend_wall * self._wall_thickness,
            self._wall_thickness,
            argb
        )

    def _draw_right_wall(
        self,
        cell: Cell,
        argb: tuple[int, int, int, int]
    ) -> None:
        extend_wall = 0
        if not cell.has_wall(Direction.SOUTH):
            extend_wall = 1
        self._draw_wall(
            (
                self._wall_total * cell.x + self._wall_total - self._wall_thickness,
                self._wall_total * cell.y
            ),
            self._wall_thickness,
            self._wall_total + extend_wall * self._wall_thickness,
            argb,
        )

    def _draw_bottom_wall(self,
        cell: Cell,
        argb: tuple[int, int, int, int],
    ) -> None:
        extend_wall = 0
        if not cell.has_wall(Direction.EAST):
            extend_wall = 1
        self._draw_wall(
            (
                cell.x * self._wall_total,
                cell.y * self._wall_total + self._wall_total - self._wall_thickness
            ),
            self._wall_total - self._wall_thickness + extend_wall * self._wall_thickness,
            self._wall_thickness,
            argb
        )

    def _draw_left_wall(self,
        cell: Cell,
        argb: tuple[int, int, int, int],
    ) -> None:
        extend_wall = 0
        if not cell.has_wall(Direction.SOUTH):
            extend_wall = 1
        self._draw_wall(
            (self._wall_total * cell.x, self._wall_total * cell.y),
            self._wall_thickness,
            self._wall_total + extend_wall * self._wall_thickness,
            argb,
        )

    def _draw_wall(
        self,
        coord: tuple[int, int],
        width: int,
        height: int,
        argb: tuple[int, int, int, int],
    ) -> None:
        for i in range(0, height):
            for j in range(0, width):
                self._image.put_pixel(
                    coord[0] + j,
                    coord[1] + i,
                    argb
                )

    def _paint_cell_background(self, cell: Cell) -> None:
        for i in range(0, self._wall_total):
            for j in range(0, self._wall_total):
                color = self._background_color if not cell.forty_two else self._wall_color
                self._image.put_pixel(
                    cell.x * self._wall_total + i,
                    cell.y * self._wall_total + j,
                    color
                )

    @property
    def image(self) -> Optional[Image]:
        return self._image
