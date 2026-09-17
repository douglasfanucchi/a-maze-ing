from typing import Any
from mlx import Mlx


class Image:
    """Wrap an MLX off-screen image and expose per-pixel drawing.

    Allocates an image through the MLX connection and keeps the raw pixel
    buffer MLX handed back, so pixels can be written directly in memory
    instead of going through the much slower per-pixel window calls. The
    buffer is only shown once the image is pushed to a window.

    Attributes:
        _conn: The MLX connection identifier the image belongs to.
        _mlx: The Mlx instance used to reach the underlying library.
        _img_ptr: The identifier MLX uses to refer to this image.
        _img_addr: A writable memoryview over the raw pixel bytes.
        _bits_per_pixel: The number of bits one pixel occupies.
        _bytes_per_pixel: The number of bytes one pixel occupies.
        _bytes_per_line: The number of bytes one row of pixels occupies.
        _endian: The pixel byte layout, 0 for B8G8R8A8, 1 for A8R8G8B8.
    """

    def __init__(
        self,
        mlx: Mlx,
        conn: Any,
        width: int,
        height: int,
    ):
        """Create an MLX image and cache its buffer layout.

        Args:
            mlx: The Mlx instance wrapping the loaded MLX library.
            conn: The MLX connection identifier returned by mlx_init.
            width: The width of the image in pixels.
            height: The height of the image in pixels.

        Raises:
            Exception: If MLX fails to allocate the image.
        """
        self._conn = conn
        self._img_ptr = mlx.mlx_new_image(conn, width, height)
        if self._img_ptr is None:
            raise Exception("Undefined error occurred while creating image")
        self._mlx = mlx
        (
            self._img_addr,
            self._bits_per_pixel,
            self._bytes_per_line,
            self._endian
        ) = mlx.mlx_get_data_addr(self._img_ptr)
        self.bytes_per_pixel = self._bits_per_pixel // 8
        # Instantly zero out the entire buffer (transparent black)
        self._img_addr[:] = b'\x00' * (self._bytes_per_line * height)

    def put_pixel(
        self,
        x: int,
        y: int,
        argb: tuple[int, int, int, int]
    ) -> None:
        """Write a single colored pixel into the image buffer.

        The colour components are ordered to match the byte layout MLX
        reported for this image, then written straight into the buffer.
        Nothing reaches the screen until the image is pushed to a window.

        Args:
            x: The horizontal coordinate of the pixel, from the left edge.
            y: The vertical coordinate of the pixel, from the top edge.
            argb: The red, green, blue and alpha components, each in the
                0-255 range. An alpha of 0 is fully transparent and 255
                is fully opaque.
        """
        pos = x * self.bytes_per_pixel + y * self._bytes_per_line
        if self._endian == 0:
            byte_val = bytes((argb[3], argb[2], argb[1], argb[0]))
        else:
            byte_val = bytes(argb)
        self._img_addr[pos:pos+4] = byte_val

    def render_on_window(self, window_addr: Any, x: int, y: int) -> Any:
        """Draw the current image content onto a window.

        Args:
            window_addr: The window identifier returned by mlx_new_window.
            x: The horizontal coordinate of the image top left corner.
            y: The vertical coordinate of the image top left corner.

        Returns:
            The status code MLX returns for the draw request.
        """
        return self._mlx.mlx_put_image_to_window(
            self._conn,
            window_addr,
            self._img_ptr,
            x,
            y
        )

    def destroy(self) -> None:
        """Release the MLX image and its pixel buffer.

        Asks MLX to free the image identified by this instance. Once it
        is destroyed, the pixel buffer is no longer valid, so the image
        must not be drawn to, rendered or destroyed again.
        """
        self._mlx.mlx_destroy_image(self._conn, self._img_ptr)
