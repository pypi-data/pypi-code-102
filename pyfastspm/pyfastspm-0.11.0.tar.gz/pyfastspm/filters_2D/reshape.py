"""This module implements basic reshaping of the raw FAST data from 1D timeseries into a sequence of 2D frames."""

import logging

import numpy as np

log = logging.getLogger(__name__)


def reshape_data(time_series, channels, x_points, y_points, num_images, num_frames):
    """
    Returns a 3D numpy array from an HDF5 file containing (image number, the 4 channels, rows).

    Args:
        time_series (1darray): the FAST data in timeseries format
        channels: a string specifying the channels to extract
        x_points (int): the number of x points
        y_points (int): the number of y points
        num_images (int): number of images
        num_frames (int): number of frames

    Returns:
        ndarray: the reshaped data as (image number, the 4 channels, rows)

    """

    data = np.reshape(time_series, (num_images, y_points * 4, x_points))

    if channels == "udf":
        data = data[:, 0 : (4 * y_points) : 2, :]
        data = np.resize(data, (num_images * 2, y_points, x_points))
        # flip every up frame upside down
        data[0 : num_frames * 2 - 1 : 2, :, :] = data[
            0 : num_frames * 2 - 1 : 2, ::-1, :
        ]

    elif channels == "udb":
        data = data[:, 1 : (4 * y_points) : 2, :]
        data = np.resize(data, (num_images * 2, y_points, x_points))
        # flip every up frame upside down
        data[0 : num_frames * 2 - 1 : 2, :, :] = data[
            0 : num_frames * 2 - 1 : 2, ::-1, :
        ]
        # flip backwards frames horizontally
        data[0 : num_frames * 2, :, :] = data[0 : num_frames * 2, :, ::-1]

    elif channels == "uf":
        data = data[:, 0 : (2 * y_points) : 2, :]
        # flip every up frame upside down
        data[0:num_frames, :, :] = data[0:num_frames, ::-1, :]
    elif channels == "ub":
        data = data[:, 1 : (2 * y_points) : 2, :]
        # flip backwards frames horizontally
        data[0:num_frames, :, :] = data[0:num_frames, :, ::-1]
        # flip every up frame upside down
        data[0:num_frames, :, :] = data[0:num_frames, ::-1, :]

    elif channels == "df":
        data = data[:, (2 * y_points) : (4 * y_points) : 2, :]
    elif channels == "db":
        data = data[:, (2 * y_points + 1) : (4 * y_points) : 2, :]
        # flip backwards frames horizontally
        data[0:num_frames, :, :] = data[0:num_frames, :, ::-1]

    elif channels == "udi":
        data = np.resize(data, (num_images * 2, y_points * 2, x_points))
        # flip backwards lines horizontally
        data[:, 1 : y_points * 2 : 2, :] = data[:, 1 : y_points * 2 : 2, ::-1]
        # flip every up frame upside down
        data[0 : num_frames * 2 - 1 : 2, :, :] = data[
            0 : num_frames * 2 - 1 : 2, ::-1, :
        ]

    elif channels == "ui":
        data = data[:, : (2 * y_points), :]
        # flip backwards lines horizontally
        data[:, 1 : y_points * 2 : 2, :] = data[:, 1 : y_points * 2 : 2, ::-1]
        # flip every up frame upside down
        data[0:num_frames, :, :] = data[0:num_frames, ::-1, :]
    elif channels == "di":
        data = data[:, (2 * y_points) :, :]
        # flip backwards lines horizontally
        data[:, 1 : y_points * 2 : 2, :] = data[:, 1 : y_points * 2 : 2, ::-1]

    else:
        raise ValueError(
            "ERROR: "
            + channels
            + " is an unsupported combination of channels in the mask"
        )
    log.info("Reshaped timeseries to movie extracting channels " + channels)
    return data
