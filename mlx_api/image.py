from typing import Any
from mlx import Mlx


class Image:
    def __init__(
        self,
        mlx: Mlx,
        conn: Any,
        width: int,
        height: int,
    ):
        self._conn = conn
        self._img_ptr = mlx.mlx_new_image(conn, width, height)
        if self._img_ptr is None:
            raise Exception("Undefined error occurred while creating image")
        self._img_ptr = self._img_ptr
        self._mlx = mlx
        addr, bpp, bpl, endian = mlx.mlx_get_data_addr(
            self._img_ptr
        )
        self._img_addr = addr
        self._bits_per_pixel = bpp
        self._bytes_per_line = bpl
        self._endian = endian

    def put_pixel(
        self,
        x: int,
        y: int,
        rgba: tuple[int, int, int, int]
    ) -> None:
        bytes_per_pixel = self._bits_per_pixel // 8
        pos = x * bytes_per_pixel + y * self._bytes_per_line
        values = [value & 0xFF for value in rgba]
        if self._endian == 1:
            values.reverse()
        for offset, value in enumerate(values):
            self._img_addr[pos + offset] = value

    def render_on_window(self, window_addr: Any, x: int, y: int) -> Any:
        return self._mlx.mlx_put_image_to_window(
            self._conn,
            window_addr,
            self._img_ptr,
            x,
            y
        )
