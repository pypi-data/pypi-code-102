import logging

import numpy as np
from scipy.ndimage import map_coordinates

log = logging.getLogger(__name__)


def pixel_trace(fast_movie, points, interpolation_order=0, mask=None):
    """Traces the value of a pixel through multiple frames in a movie.
    Supports averaging in an arbitrary mask around the pixel, and linear drift interpolation through
    a specified set of points.

    Args:
        fast_movie: a FastMovie instance
        points: a dictionary with one or more elements in the following format::

                  {<frame number>: (<x coordinate>, <y coordinate>)}

                where the frame numbers must be monotonically increasing.
        interpolation_order: order of the interpolation for the point position (0-5)
        mask: an array representing a mask where the image will be averaged around the selected points

    Returns:
        dict: a dictionary with the following entries, each containing an array representing:

                - ``'value'``: the value of the pixels
                - ``'timestamps'``: the timestamps of each position
                - ``'frames'``: the frame number the pixel belongs to
                - ``'x_pos'``: the x position of the tracked pixel
                - ``'y_pos'``: the y position of the tracked pixel


    Notes:
        The point can also have non-integer coordinates, in which case interpolation is used.
        The calculated center of the mask array (regardless of its contents) will be centered
        on the point that is being traced.

    Example:
        >>> pixel_trace(mov, {0: (12.3, 56.3)}, interpolation_order=3)

    """
    key_frame_list = sorted(list(points.keys()))

    if len(points) == 1:
        start_frame = 0
        end_frame = fast_movie.data.shape[0] - 1
        points = {0: points[key_frame_list[0]]}
        print(points)
    else:
        start_frame = key_frame_list[0]
        end_frame = key_frame_list[-1]

    num_frames = end_frame - start_frame + 1

    trace = {
        "timestamps": np.zeros(num_frames, dtype=np.float),
        "x_pos": np.zeros(num_frames, dtype=np.float),
        "y_pos": np.zeros(num_frames, dtype=np.float),
        "frames": np.zeros(num_frames, dtype=np.uint32),
        "values": np.zeros(num_frames, dtype=np.float),
    }

    # build a dictionary of the position increments per each key frame pairs
    increments = {}
    for idx in range(len(key_frame_list) - 1):
        dx = points[key_frame_list[idx + 1]][0] - points[key_frame_list[idx]][0]
        dx /= key_frame_list[idx + 1] - key_frame_list[idx]
        dy = points[key_frame_list[idx + 1]][1] - points[key_frame_list[idx]][1]
        dy /= key_frame_list[idx + 1] - key_frame_list[idx]
        increments[key_frame_list[idx]] = (dx, dy)

    if mask is None:
        mask = np.array([[1]])
        mask_x_center = mask_y_center = 0.0
    else:
        mask_x_center = (mask.shape[0] - 1) / 2
        mask_y_center = (mask.shape[1] - 1) / 2
    x_mask, y_mask = np.where(mask == 1)

    x, y = points[key_frame_list[0]]
    dx = dy = 0.0
    for idx, frame in enumerate(range(start_frame, end_frame + 1)):
        trace["timestamps"][idx] = frame / fast_movie.fps
        trace["x_pos"][idx] = x
        trace["y_pos"][idx] = y
        trace["frames"][idx] = np.uint32(frame)
        mask_coords = np.vstack(
            (x_mask + x - mask_x_center, y_mask + y - mask_y_center)
        )
        trace["values"][idx] = map_coordinates(
            fast_movie.data[frame, :, :].astype(np.float),
            mask_coords,
            order=interpolation_order,
        ).mean()
        if frame in key_frame_list[:-1]:
            dx, dy = increments[frame]
        x += dx
        y += dy

    return trace


def time_series_fft(h5file, time_series=None, num_points=None):
    """Calculates the 1D-FFT of a time series.

    Calculates the 1D-FFT of a time series. The signal sampling parameters are
    taken from the ``h5`` file.

    Args:
        h5file (h5py.File): an instance of ``h5py.File``
        time_series (1darray, optional): the time series input for the FFT
            operation
        num_points (int, optional): the number of points of the FFT. Recall
            that the relationship between the frequency resolution
            :math:`\\Delta f` of the FFT and the number of points :math:`N`
            is given by

            .. math:: \\Delta f = \\frac{f_s}{N}

            where :math:`f_s` is the sampling frequency.

    Returns:
        2darray: the first column is the frequency and second is the magnitude

    Todo:
        Implement the FFT. Check if maybe the Power Spectral Density is the
        best way to look at the data. See `this link
        <http://docs.scipy.org/doc/scipy-dev/reference/generated/scipy
        .signal.welch.html>`_ for more info.

    """

    pass
