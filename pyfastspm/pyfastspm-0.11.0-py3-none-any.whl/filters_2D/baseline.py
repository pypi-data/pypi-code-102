"""This module adds a 2D plane subtraction and baseline subtraction"""

import logging
from copy import copy
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

from ..fast_movie import FastMovie

log = logging.getLogger(__name__)


def _baselines(frame, par_baseline, baseline_type):
    """Estimates the baselines of a frame in y and x direction

    Args:
        frame: the frame
        par_baseline: if baseline_type='mean', defines how much of the histogram at the top and bottom
            is considered outliers or features and is not averaged over; has no influence otherwise
        baseline_type: 'median' or 'mean'

    Returns:
        baseline_y: baseline in y direction
        baseline_x: baseline in x direction

    """
    if baseline_type == "mean":
        # Row by row / line by line averaging of the background along both axes.
        # The top and bottom par_baseline*100% are considered outliers or features
        # and are not accounted for in the averaging.

        ny = frame.shape[0]
        nx = frame.shape[1]

        fraction_y = int(ny * par_baseline)
        fraction_x = int(nx * par_baseline)

        baseline_y = np.zeros(ny)
        baseline_x = np.zeros(nx)

        for i in range(ny):
            unsorted_x = frame[i, :].flatten()
            sorted_bot_x = unsorted_x[np.argpartition(unsorted_x, ny - fraction_y)]
            bottom_x = sorted_bot_x[: ny - fraction_y]
            sorted_top_x = bottom_x[np.argpartition(-bottom_x, ny - 2 * fraction_y)]
            top_x = sorted_top_x[: ny - 2 * fraction_y]
            baseline_y[i] = np.mean(top_x)
        for j in range(nx):
            unsorted_y = frame[:, j].flatten()
            sorted_bot_y = unsorted_y[np.argpartition(unsorted_y, nx - fraction_x)]
            bottom_y = sorted_bot_y[: nx - fraction_x]
            sorted_top_y = bottom_y[np.argpartition(-bottom_y, nx - 2 * fraction_x)]
            top_y = sorted_top_y[: nx - 2 * fraction_x]
            baseline_x[j] = np.mean(top_y)

    elif baseline_type == "median":
        baseline_y = np.median(frame, 1)
        baseline_x = np.median(frame, 0)

    return baseline_y, baseline_x


def plane_2D(
    fast_movie: FastMovie, par_baseline=0.16, baseline_type="median", image_range=None
):
    """Corrects for sample tilting by subtraction of a plane.

    Args:
        fast_movie: (FastMovie) an instance of the FastMovie class
        par_baseline: if baseline_type='mean', defines how much of the histogram at the top and bottom
            is considered outliers or features and is not averaged over; has no influence otherwise
        baseline_type: defines how the baselines in y and x direction are estimated; 'median' (default) or 'mean'
        image_range: an int or a tuple indicating the image range to correct

    Returns:
        nothing

    """

    if fast_movie.mode != "movie":
        raise ValueError("you must first reshape your data in movie mode.")

    ny = fast_movie.data.shape[1]
    nx = fast_movie.data.shape[2]
    y = np.linspace(-0.5, 0.5, ny)
    x = np.linspace(-0.5, 0.5, nx)

    fast_movie.processing_log.info(
        "2D plane subtraction on image_range {}. `{}` baseline_type baseline with par_baseline = {:05.4f}.".format(
            image_range, baseline_type, par_baseline
        )
    )

    for _, _, frame in tqdm(
        fast_movie.iter_frames(image_range=image_range),
        desc="2D plane correction",
        unit="frames",
    ):
        by, bx = _baselines(fast_movie.data[frame], par_baseline, baseline_type)

        tilt_y, _ = np.polyfit(y, by, 1)
        tilt_x, _ = np.polyfit(x, bx, 1)

        y_corr = -y * tilt_y
        x_corr = -x * tilt_x

        for i in range(nx):
            fast_movie.data[frame, :, i] += y_corr
        for i in range(ny):
            fast_movie.data[frame, i, :] += x_corr


def plot_baseline(
    fast_movie: FastMovie, frame, par_baseline=0.16, baseline_type="median"
):
    """Plots the baselines of a frame

    Args:
        fast_movie: (FastMovie) an instance of the FastMovie class
        frame: frame index
        par_baseline: if baseline_type='mean', defines how much of the histogram at the top and bottom
            is considered outliers or features and is not averaged over; has no influence otherwise
        baseline_type: defines how the baselines in y and x direction are estimated; 'median' (default) or 'mean'

    Returns:
        nothing

    """

    if fast_movie.mode != "movie":
        raise ValueError("you must first reshape your data in movie mode.")

    ny = fast_movie.data.shape[1]
    nx = fast_movie.data.shape[2]
    y = np.linspace(-0.5, 0.5, ny)
    x = np.linspace(-0.5, 0.5, nx)

    by, bx = _baselines(fast_movie.data[frame], par_baseline, baseline_type)

    plt.plot(x, bx, "-", label="x")
    plt.plot(y, by, "-", label="y")

    plt.legend()
    plt.tight_layout()
    plt.show()


def baseline_corr(
    fast_movie: FastMovie,
    corr_y=True,
    corr_x=False,
    par_baseline=0.16,
    baseline_type="median",
    image_range=None,
):
    """Baseline correction

    Args:
        fast_movie: (FastMovie) an instance of the FastMovie class
        corr_y: Boolean indicating whether the baseline in y direction should be subtracted; defaults to True
        corr_x: Boolean indicating whether the baseline in x direction should be subtracted; defaults to False
        par_baseline: if baseline_type='mean', defines how much of the histogram at the top and bottom
            is considered outliers or features and is not averaged over; has no influence otherwise
        baseline_type: defines how the baselines in y and x direction are estimated; 'median' (default) or 'mean'
        image_range: an int or a tuple indicating the image range to correct

    Returns:
        nothing

    """

    if fast_movie.mode != "movie":
        raise ValueError("you must first reshape your data in movie mode.")

    ny = fast_movie.data.shape[1]
    nx = fast_movie.data.shape[2]

    if corr_y:
        fast_movie.processing_log.info(
            "y baseline subtraction on image_range {}. `{}` baseline_type baseline with par_baseline = {:05.4f}.".format(
                image_range, baseline_type, par_baseline
            )
        )
    if corr_x:
        fast_movie.processing_log.info(
            "x baseline subtraction on image_range {}. `{}` baseline_type baseline with par_baseline = {:05.4f}.".format(
                image_range, baseline_type, par_baseline
            )
        )

    for _, _, frame in tqdm(
        fast_movie.iter_frames(image_range=image_range),
        desc="Baseline correction",
        unit="frames",
    ):
        by, bx = _baselines(fast_movie.data[frame], par_baseline, baseline_type)
        if corr_y:
            for i in range(nx):
                fast_movie.data[frame, :, i] -= by
        if corr_x:
            for i in range(ny):
                fast_movie.data[frame, i, :] -= bx
