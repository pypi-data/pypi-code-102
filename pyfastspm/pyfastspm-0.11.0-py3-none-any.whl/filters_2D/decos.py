"""Decos functions"""

import numpy as np
from scipy.interpolate import RectBivariateSpline
from tqdm import tqdm

from ..fast_movie import FastMovie


class TruePixel:
    """A TruePixel is a representation of the pixel after decos

    A TruePixel represents real pixels, that have equal spatial extension,
    as opposed to raw pixels that when acquired by FAST, have a non-uniform
    spatial extension.

    Attributes:
        nx: the number of pixels in the image.

    """

    def __init__(self, nx):
        self.nx = nx
        # self.ny = ny

    def start(self, n):
        """Returns the starting position of the n-th true_pixel expressed as raw_pixel coordinate"""
        if 0 <= n <= self.nx:
            return np.arccos(2.0 / self.nx * (self.nx - n) - 1.0) / np.pi * self.nx
        else:
            return np.nan

    def end(self, n):
        """Return the end position of the n-th true_pixel expressed as raw_pixel coordinate"""
        if 0 <= n <= self.nx:
            return (
                np.arccos(2.0 / self.nx * (self.nx - (n + 1)) - 1.0) / np.pi * self.nx
            )
        else:
            return np.nan

    def max_pixel_length(self):
        """Return the maximum length of the true_pixels"""
        return self.end(0) - self.start(0)

    def frac_raw_pixel(self, true_pixel, raw_pixel):
        """Return the fraction of a given raw_pixel contained in the given true_pixel"""
        if self.start(true_pixel) <= raw_pixel and self.end(true_pixel) >= (
            raw_pixel + 1
        ):
            # raw_pixel is entirely contained in true_pixel
            return 1.0
        elif self.end(true_pixel) < raw_pixel or self.start(true_pixel) > (
            raw_pixel + 1
        ):
            # raw_pixel does not overlap true_pixel
            return 0.0
        elif self.start(true_pixel) > raw_pixel and self.end(true_pixel) < (
            raw_pixel + 1
        ):
            # true_pixel is entirely contained in a raw_pixel
            return self.end(true_pixel) - self.start(true_pixel)
        elif self.start(true_pixel) > raw_pixel and self.end(true_pixel) >= (
            raw_pixel + 1
        ):
            # true_pixel bleeds out on the right side of raw_pixel
            return raw_pixel + 1 - self.start(true_pixel)
        elif self.start(true_pixel) <= raw_pixel and self.end(true_pixel) < (
            raw_pixel + 1
        ):
            # true_pixel bleeds out on the left side of raw_pixel
            return self.end(true_pixel) - raw_pixel
        elif (
            true_pixel < 0
            or true_pixel > self.nx
            or raw_pixel < 0
            or raw_pixel > self.nx
        ):
            # trim to zero the cases where pixel indices are negative or bigger
            # than nx
            return 0.0
        else:
            raise Exception(
                "IMPLEMENTATION ERROR: pixel weighting slipped out of cases! This is BAD news."
            )


def __generate_decos_kernel(nx):
    """Generate the kernel required for the "lossless" decos of the frames

    Args:
        nx (int): the number of pixels in the fast scan direction

    Returns:
        kernel (array): returns a num_pixels X numpixels array containing the
            required kernel
    """

    true_pixel = TruePixel(nx)
    kernel_size = np.ceil(true_pixel.max_pixel_length())
    kernel = np.zeros((true_pixel.nx, true_pixel.nx))
    for pixel in np.arange(0, true_pixel.nx):
        for ker in np.arange(0, kernel_size):
            raw_pixel = int(np.floor(true_pixel.start(pixel)) + ker)
            kernel[pixel, raw_pixel] = true_pixel.frac_raw_pixel(pixel, raw_pixel)
    return kernel


def accurate_decos(fast_movie: FastMovie, image_range=None, kernel=None):
    """Corrects cosine distortion in a frame or a movie with high accuracy using
    a variable kernel weighting of the pixels.

    Args:
        fast_movie: (FastMovie) an instance of the FastMovie class
        image_range: an int or a tuple indicating the image range to decos
        kernel: (optional) provide the kernel for the decos operation

    Returns:
        a modified version the FastMovie.data attribute
    """
    if fast_movie.mode != "movie":
        raise ValueError("you must first reshape your data in movie mode.")

    if image_range is None:
        image_range = fast_movie.full_image_range

    if isinstance(image_range, int):
        image_range = (image_range,)

    nx = fast_movie.data.shape[2]
    ny = fast_movie.data.shape[1]

    if kernel is None:
        kernel = __generate_decos_kernel(nx)

    for _, _, frame in tqdm(
        fast_movie.iter_frames(image_range=image_range),
        desc="accurate decos",
        unit="frames",
    ):
        decos = np.zeros((ny, nx), dtype=np.float16)
        for col in range(0, nx, 1):
            b = np.asarray([kernel[col, :]] * ny)
            decos[:, col] = (fast_movie.data[frame, :, :] * b).sum(1) / b.sum(1)
        fast_movie.data[frame, :, :] = decos


def quick_decos(fast_movie: FastMovie, image_range=None):
    """Corrects cosine distortion in a frame or a movie with fast re-sampling onto
    an appropriate meshgrid.

    Args:
        fast_movie: (FastMovie) an instance of the FastMovie class
        image_range: an int or a tuple indicating the image range to decos

    Returns:
        a modified version the FastMovie.data attribute

    References:
        Alexander Jussupow, *Analysis of fast-STM movies using Python* -
        Research internship report - Department of Chemistry, TU Munich (2014)

    """
    if fast_movie.mode != "movie":
        raise ValueError("you must first reshape your data in movie mode.")

    if image_range is None:
        image_range = fast_movie.full_image_range

    if isinstance(image_range, int):
        image_range = (image_range,)

    nx = fast_movie.data.shape[2]
    ny = fast_movie.data.shape[1]
    t1 = np.linspace(-(ny / 2), ny / 2, ny)
    t2 = np.linspace(-(nx / 2), nx / 2, nx)
    # hysteresis in x direction
    x2 = nx / 2.0 * np.sin(t2 * np.pi / (nx))
    for _, _, frame in tqdm(
        fast_movie.iter_frames(image_range=image_range),
        desc="quick decos",
        unit="frames",
    ):
        f2D = RectBivariateSpline(t1, x2, fast_movie.data[frame])
        fast_movie.data[frame] = f2D(t1, t2)
