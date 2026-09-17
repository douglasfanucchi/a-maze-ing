from .maze_image import MazeImage
from mazegen.direction import Direction
from typing import Generator, Any
from mazegen import MazeGenerator


class WallsImage(MazeImage):
    def __init__(
        self,
        mlx: Any,
        mlx_conn: Any,
        maze: MazeGenerator,
        width: int,
        height: int,
        wall_thickness: float,
        background_color: tuple[int, int, int, int],
        color: tuple[int, int, int, int]
    ):
        super().__init__(mlx, mlx_conn, maze, width, height, wall_thickness)
        self._background_color = background_color
        self._wall_color = color
        self._create_grid()

    def _create_grid(self) -> None:
        for row in self._maze.grid.matrix:
            for cell in row:
                for direction in Direction:
                    self._paint_wall(
                        (cell.x, cell.y),
                        direction,
                        self._wall_color
                    )
                self._paint_corners((cell.x, cell.y), (0, 0), self._wall_color)
                self._paint_corners((cell.x, cell.y), (1, 0), self._wall_color)
                self._paint_corners((cell.x, cell.y), (0, 1), self._wall_color)
                self._paint_corners((cell.x, cell.y), (1, 1), self._wall_color)

    def render_frames(self, win_ptr: Any, coords: tuple[int, int]) -> Generator:
        for row in self._maze.grid.matrix:
            for cell in row:
                for direction in Direction:
                    if not cell.has_wall(direction):
                        self._paint_wall(
                            (cell.x, cell.y),
                            direction,
                            self._background_color
                        )
        while True:
            self._image.render_on_window(win_ptr, *coords)
            yield
