"""Module for rendering a maze grid onto an MLX image canvas."""

from mlx import Mlx  # type: ignore[import-untyped, unused-ignore]
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

    Attributes:
    _maze: The MazeGenerator instance containing grid data.
    _cell_total: total pixel size of a single square cell block
        (includes both the empty interior and its surrounding walls).
    _image: MLX wrapper instance for off-screen image
    _wall_thickness: Pixel thickness of the drawn wall lines and corners.
    _cell_interior: The pixel width/height of the empty background area inside
        the square cell where a path can be drawn.
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
        self._image = Image(mlx, mlx_conn, width, height)
        cell_total_pre: int = min(
            width // maze.grid.width,
            height // maze.grid.height
        )
        wall_thickness_pre: int = max(
            1,
            int(cell_total_pre * wall_thickness) // 100
        )
        self._cell_total = min(
            (width - wall_thickness_pre * 2) // maze.grid.width,
            (height - wall_thickness_pre * 2) // maze.grid.height
        )
        self._wall_thickness = max(
            1,
            int(self._cell_total * wall_thickness) // 100
        )
        self._cell_interior = max(
            1, self._cell_total - (self._wall_thickness * 2)
        )

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

    def draw_maze(
        self,
        wall_color: tuple[int, int, int, int] = (0, 0, 0, 255),
        bg_color: tuple[int, int, int, int] = (255, 255, 255, 255),
        entry_color: tuple[int, int, int, int] = (0, 255, 0, 255),
        exit_color: tuple[int, int, int, int] = (255, 0, 0, 255),
        pattern_color: tuple[int, int, int, int] = (100, 100, 100, 255)
    ) -> None:
        """Render the complete maze state onto the image buffer.

        Args:
            wall_color: ARGB color for active walls and corner posts.
            bg_color: ARGB color for standard corridor interiors.
            entry_color: ARGB color for the entry cell.
            exit_color: ARGB color for the exit cell.
            pattern_color: ARGB color for reserved 42 pattern cells.
        """
        # Calculate total pixel bounds of the padded maze
        maze_w = (
            self._maze.grid.width * self._cell_total
            + (self._wall_thickness * 2)
        )
        maze_h = (
            self._maze.grid.height * self._cell_total
            + (self._wall_thickness * 2)
        )

        # Draw the 4 outer frame edges to seal the maze
        self._fill_rect(0, 0, maze_w, self._wall_thickness, wall_color)
        self._fill_rect(
            0, maze_h - self._wall_thickness,
            maze_w, self._wall_thickness,
            wall_color
        )
        self._fill_rect(0, 0, self._wall_thickness, maze_h, wall_color)
        self._fill_rect(
            maze_w - self._wall_thickness, 0,
            self._wall_thickness, maze_h,
            wall_color
        )

        for row in self._maze.grid.matrix:
            for cell in row:
                if cell is None:
                    continue
                cell_coords = (cell.x, cell.y)
                # Determine cell interior color
                color = bg_color
                if cell_coords == self._maze.entry:
                    color = entry_color
                elif cell_coords == self._maze.exit:
                    color = exit_color
                elif cell.forty_two:
                    color = pattern_color
                # Paint interior background
                self._paint_cell_background(cell, color)
                # Paint active walls
                for direction in Direction:
                    if cell.has_wall(direction):
                        self._paint_wall(cell_coords, direction, wall_color)
                # Paint corner posts only if the joint is active
                if self._is_joint_active(cell.x, cell.y):
                    self._paint_corners((cell.x, cell.y), (0, 0), wall_color)
                if self._is_joint_active(cell.x + 1, cell.y):
                    self._paint_corners((cell.x, cell.y), (1, 0), wall_color)
                if self._is_joint_active(cell.x, cell.y + 1):
                    self._paint_corners((cell.x, cell.y), (0, 1), wall_color)
                if self._is_joint_active(cell.x + 1, cell.y + 1):
                    self._paint_corners((cell.x, cell.y), (1, 1), wall_color)

    def _fill_rect(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: tuple[int, int, int, int]
    ) -> None:
        """Fill a rectangular region on the image buffer.

        Args:
            x: Starting horizontal coordinate.
            y: Starting vertical coordinate.
            w: Width of the rectangle in pixels.
            h: Height of the rectangle in pixels.
            color: ARGB tuple to paint.
        """
        for i in range(w):
            for j in range(h):
                self._image.put_pixel(x + i, y + j, color)

    def _paint_wall(
        self,
        coords: tuple[int, int],
        direction: Direction,
        color: tuple[int, int, int, int]
    ) -> None:
        """Paint a single wall segment in the given direction.

        Args:
            coords: (x, y) cell grid coordinates.
            direction: Direction of the wall segment.
            color: ARGB color to paint.
        """
        px = coords[0] * self._cell_total + self._wall_thickness
        py = coords[1] * self._cell_total + self._wall_thickness
        if direction in (Direction.NORTH, Direction.SOUTH):
            px += self._wall_thickness
            if direction == Direction.SOUTH:
                py += self._wall_thickness + self._cell_interior
            self._fill_rect(
                px, py, self._cell_interior, self._wall_thickness, color
            )
        else:
            py += self._wall_thickness
            if direction == Direction.EAST:
                px += self._wall_thickness + self._cell_interior
            self._fill_rect(
                px, py, self._wall_thickness, self._cell_interior, color
            )

    def _paint_corners(
        self,
        coords: tuple[int, int],
        vector: tuple[int, int],
        color: tuple[int, int, int, int]
    ) -> None:
        """Paint a corner joint post.

        Args:
            coords: (x, y) cell grid coordinates.
            vector: (dx, dy) corner offset.
                (0, 0): top-left
                (1, 0): top-right
                (0, 1): bottom-left
                (1, 1): bottom-right
            color: ARGB color to paint.
        """
        px = (
            coords[0] * self._cell_total
            + vector[0] * (self._cell_interior + self._wall_thickness)
            + self._wall_thickness
        )
        py = (
            coords[1] * self._cell_total
            + vector[1] * (self._cell_interior + self._wall_thickness)
            + self._wall_thickness
        )
        self._fill_rect(
            px, py, self._wall_thickness, self._wall_thickness, color
        )

    def _is_joint_active(self, jx: int, jy: int) -> bool:
        """Check if a corner joint intersection has any connecting walls.

        Args:
            jx: The grid X coordinate of the joint.
            jy: The grid Y coordinate of the joint.

        Returns:
            True if any of the 4 radiating walls exist, False otherwise.
        """
        # Check the cell to the bottom-right of the joint
        c_br = self._maze.grid.get_cell(jx, jy)
        if (
            c_br and
            (c_br.has_wall(Direction.NORTH) or c_br.has_wall(Direction.WEST))
        ):
            return True
        # Check the cell to the bottom-left of the joint
        c_bl = self._maze.grid.get_cell(jx - 1, jy)
        if (
            c_bl and
            (c_bl.has_wall(Direction.NORTH) or c_bl.has_wall(Direction.EAST))
        ):
            return True
        # Check the cell to the top-right of the joint
        c_tr = self._maze.grid.get_cell(jx, jy - 1)
        if (
            c_tr and
            (c_tr.has_wall(Direction.WEST) or c_tr.has_wall(Direction.SOUTH))
        ):
            return True
        # Check the cell to the top-left of the joint
        c_tl = self._maze.grid.get_cell(jx - 1, jy - 1)
        if (
            c_tl and
            (c_tl.has_wall(Direction.EAST) or c_tl.has_wall(Direction.SOUTH))
        ):
            return True
        return False

    def _paint_cell_background(
        self,
        cell: Cell,
        color: tuple[int, int, int, int]
    ) -> None:
        """Fill the interior area of a cell.

        Args:
            cell: Target Cell object.
            color: ARGB color to paint.
        """
        px = cell.x * self._cell_total + self._wall_thickness * 2
        py = cell.y * self._cell_total + self._wall_thickness * 2
        self._fill_rect(
            px, py, self._cell_interior, self._cell_interior, color
        )
