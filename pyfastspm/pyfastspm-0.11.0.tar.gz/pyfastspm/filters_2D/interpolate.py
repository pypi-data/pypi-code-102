"""Exact interpolation for interlacing"""

import logging
import math
from copy import copy

import numpy as np
from scipy.interpolate import griddata, splev, splrep
from scipy.optimize import curve_fit
from scipy.signal import correlate
from scipy.sparse import csr_matrix, lil_matrix
from scipy.spatial import Delaunay
from tqdm import tqdm

from ..fast_movie import FastMovie

log = logging.getLogger(__name__)


def _Bezier(y, shape, pixels, Bezier_points):
    """Corrects a given y meshgrid for probe creep, using a Bezier curve

    Args:
        y: y meshgrid
        ny: number of pixels in y direction
        shape: 3-tuple describing the shape of the creep in y direction; see wiki for further information
        pixels: excess pixels at top/bottom in up/down frames
        Bezier_points: number of grid points for the numeric creep function

    Returns:
        y_up, y_down: corrected y meshgrids in both scan directions

    """

    ny = y.shape[0]

    # different creep in up and down frames
    y_up = copy(y)
    y_down = copy(y)

    ind_up = int(
        ny * (1.0 - shape[0])
    )  # point at which the y movement becomes linear in upward frames
    ind_down = int(ny * shape[0])

    # creep is approximated by a Bezier curve
    P0_up = np.array([min(y[ind_up, :]), min(y[ind_up, :])])
    P12_up = np.array([y[-1, 0] - pixels, y[-1, 0] - pixels])
    P3_up = np.array([y[-1, 0], y[-1, 0] - pixels])

    P1_up = (1.0 - shape[1]) * P0_up + shape[1] * P12_up
    P2_up = (1.0 - shape[2]) * P12_up + shape[2] * P3_up

    # since Bezier curves have the form (x,y)(t) rather than y(x), one has to numerically find y(x) on a grid
    t = np.linspace(0.0, 1.0, Bezier_points)

    Bezier_up = np.array(
        [
            (1 - t) ** 3 * P0_up[0]
            + 3 * (1 - t) ** 2 * t * P1_up[0]
            + 3 * (1 - t) * t ** 2 * P2_up[0]
            + t ** 3 * P3_up[0],
            (1 - t) ** 3 * P0_up[1]
            + 3 * (1 - t) ** 2 * t * P1_up[1]
            + 3 * (1 - t) * t ** 2 * P2_up[1]
            + t ** 3 * P3_up[1],
        ]
    )

    j = 0  # initialize j only once to avoid the algorithm searching the entire Bezier curve for each y element
    for i, yi in enumerate(y_up[ind_up:, :]):
        ind = ind_up + i  # actual index of the line in the original array
        fb = (-1) ** (ind % 2)  # 1 for forward, -1 for backward
        for ii, yii in enumerate(
            yi[::fb]
        ):  # restore time ordering which is lost by reshaping
            while j < Bezier_points:
                if (
                    Bezier_up[0, j] >= yii
                ):  # find the index at which the Bezier curve passes yii
                    break
                j += 1
            w0 = yii - Bezier_up[0, j - 1]
            w1 = Bezier_up[0, j] - yii
            y_up[ind, ::fb][ii] = (w0 * Bezier_up[1, j] + w1 * Bezier_up[1, j - 1]) / (
                w0 + w1
            )  # linear interpolation between two Bezier points

    P3_down = np.array([max(y[ind_down, :]), max(y[ind_down, :])])
    P12_down = np.array([y[0, 0] + pixels, y[0, 0] + pixels])
    P0_down = np.array([y[0, 0], y[0, 0] + pixels])

    P2_down = (1.0 - shape[1]) * P3_down + shape[1] * P12_down
    P1_down = (1.0 - shape[2]) * P12_down + shape[2] * P0_down

    Bezier_down = np.array(
        [
            (1 - t) ** 3 * P0_down[0]
            + 3 * (1 - t) ** 2 * t * P1_down[0]
            + 3 * (1 - t) * t ** 2 * P2_down[0]
            + t ** 3 * P3_down[0],
            (1 - t) ** 3 * P0_down[1]
            + 3 * (1 - t) ** 2 * t * P1_down[1]
            + 3 * (1 - t) * t ** 2 * P2_down[1]
            + t ** 3 * P3_down[1],
        ]
    )

    j = 0
    for i, yi in enumerate(y_down[:ind_down, :]):
        fb = (-1) ** (i % 2)
        for ii, yii in enumerate(yi[::fb]):
            while j < Bezier_points:
                if Bezier_down[0, j] >= yii:
                    break
                j += 1
            w0 = yii - Bezier_down[0, j - 1]
            w1 = Bezier_down[0, j] - yii
            y_down[i, ::fb][ii] = (
                w0 * Bezier_down[1, j] + w1 * Bezier_down[1, j - 1]
            ) / (w0 + w1)

    # shift everything, such that endpoints match
    y_down -= pixels / 2.0
    y_up += pixels / 2.0

    return y_up, y_down


def _output_y_grid(ny, nx):
    """Returns the y grid of the data points; not corrected for probe creep

    Args:
        ny: number of pixels in y direction
        nx: number of pixels in x direction

    Returns:
        y:  y meshgrid of measured datapoints
        t1: equidistant 1D grid; contains the centers of each line in y

    """

    # equidistant grid
    t1 = np.linspace(-(ny / 2), ny / 2, ny)

    # hysteresis in y direction
    dy = np.abs(t1[0] - t1[1])
    y_drift = np.linspace(-(dy / 2), dy / 2, nx)

    # meshgrid of measured datapoints
    y = np.array([y_drift * (-1) ** (j) + t1[j] for j in range(ny)])

    return y, t1


def _output_x_grid(ny, nx):
    """Returns the x grid of the data points

    Args:
        ny: number of pixels in y direction
        nx: number of pixels in x direction

    Returns:
        x:  x meshgrid of measured datapoints
        t2: equidistant 1D grid

    """

    # equidistant grid
    t2 = np.linspace(-(nx / 2), nx / 2, nx)

    # hysteresis in x direction
    x2 = nx / 2.0 * np.sin(t2 * np.pi / (nx))

    # meshgrid of measured datapoints
    x = np.array([x2 for j in range(ny)])

    return x, t2


def _interpolate_col(col, y):
    """Spline interpolation of a single column on a given y grid

    Args:
        col: the column
        y: y grid of the data in col

    Returns:
        col_int: interpolated data on an equidistant grid of the same size as the original grid

    """

    t1 = np.linspace(min(y), max(y), len(y))

    tck = splrep(y, col, s=0)
    col_int = splev(t1, tck, der=0)

    return col_int


def _interpolate_col_param(input1, shape1, shape2, shape3, pixels):
    """Given the shape parameters and pixel number for the creep correction,
    compares the interpolated data of a column in an up and a down frame

    Args:
        input1: 5-tuple containing:
            y: not creep corrected y grid of the column
            up: data of the column in the up frame
            down: data of the column in the down frame
            Bezier_points: number of grid points for the numeric creep function
            w: additional weighting of the lines at the upper and lower boundary; weight function is w*y**2/max(y)**2 + 1
        shape1, shape2, shape3: shape parameters for creep correction
        pixels: pixel number for creep correction

    Returns:
        on equidistant grid: difference between interpolated up and down column times the weight function

    """
    y, up, down, Bezier_points, w = input1

    y_up, y_down = _Bezier(
        np.reshape(y, (len(y), 1)), (shape1, shape2, shape3), pixels, Bezier_points
    )

    up_int = _interpolate_col(up, y_up)
    down_int = _interpolate_col(down, y_down)

    weight = w * y ** 2 / max(y) ** 2 + 1

    return (up_int - down_int) * weight


def fit_creep(
    fast_movie: FastMovie,
    col_inds,
    images,
    w=0.0,
    shape=(0.5, 2.0 / 3.0, 1.0 / 3.0),
    pixels=0,
    Bezier_points=1000,
):
    """Fits the shape parameters and pixel number for creep correction to minimize
    the difference between interpolated columns in up and a down frames

    Args:
        fast_movie: FastMovie object
        col_inds: n-tuple of indices of the columns to fit
        images: n-tuple of indices of the images to fit
        w: additional weighting of the lines at the upper and lower boundary;
            weight function is w*y**2/max(y)**2 + 1
            defaults to 0
        shape: 3-tuple containing the initial guess for the shape parameters;
            defaults to (.5, 2./3., 1./3.)
        pixels: initial guess for the pixel number
        Bezier_points: number of grid points for the numeric creep function

    Returns:
        opt: 4 element array containing the fitted shape parameters and pixel number (in this order)

    """

    if "i" not in fast_movie.channels:
        raise ValueError("Interpolation currently only available for interlacing")

    if fast_movie.mode != "movie":
        raise ValueError("you must first reshape your data in movie mode.")

    fast_movie.processing_log.info(
        "Fitting creep correction at columns {} in images {}. Initial guess: shape = ({:05.4f}, {:05.4f}, {:05.4f}), pixels = {:05.4f}.".format(
            col_inds, images, shape[0], shape[1], shape[2], pixels
        )
    )
    fast_movie.processing_log.info(
        "Additional weight to top and bottom image boundary: {}. Number of evaluation points for numeric creep function: {}.".format(
            w, Bezier_points
        )
    )

    nx = fast_movie.data.shape[2]
    ny = fast_movie.data.shape[1]

    y_full, _ = _output_y_grid(ny, nx)

    opt_list = []

    for col_ind in col_inds:
        y = y_full[:, col_ind]

        for image in images:
            up = fast_movie.data[image * 2, :, col_ind]
            down = fast_movie.data[image * 2 + 1, :, col_ind]
            opt_i, _ = curve_fit(
                _interpolate_col_param,
                (y, up, down, Bezier_points, w),
                np.zeros_like(up),
                (shape[0], shape[1], shape[2], pixels),
                bounds=([0.1, 0.0, 0.0, 0], [1.0, 1.0, 1.0, 20]),
            )

            opt_list.append(opt_i)

    opt = np.mean(np.array(opt_list), 0)

    fast_movie.processing_log.info(
        "Optimized creep parameters for later use: shape = ({:05.4f}, {:05.4f}, {:05.4f}), pixels = {:05.4f}".format(
            opt[0], opt[1], opt[2], opt[3]
        )
    )

    return opt


def get_interpolation_matrix(
    points_to_triangulate, grid_points
):  # grid_points has to be a list of tuples!

    """
    Creates matrix containing all the relevant information for interpolating
    values measured at the same relative postion to a grid.

    The matix is constructed in a sparse format to limit memory usage.
    Construction is done in the lil sparse format, which is late converted to csr format for
    faster matrix vector dot procut.

    The matrix is of the form  (number of grid points at which to interpolate the frame) x (number of measured points within one frame).
    For this reason the number of interpolation and measured points do not have to be the same.

    Frames are interpolated within one matrix vecor dot product. For this reason the frame arrays
    need to be flattened (vectorized) before multiplication.

    Args:
        points_to_triangulate: list of tuples! represnting the points of measurement
        grid_points: list of tuples! represnting the grid points at which to interpolate

    The input formatting is slightly unusuall if you are used to numpy etc.
    Here we do not give two list, each containing values for one dimension.
    Insted we give tuples of values for each point i.e. (x,y) - See QHull documentation.

    Steps:
        1) Perform delaunay triangulation on grid of measurement positions.
        2) Find dealaunay triangles which contain new grid points.
        3) For each triangle get indices of corner poinst.
        4) At corresponding point in matrix insert barycentric coordinates.
    """

    triangulation = Delaunay(points_to_triangulate)
    triangles_containing_gridpoints = triangulation.find_simplex(grid_points)
    interpolation_matrix = lil_matrix((len(grid_points), len(points_to_triangulate)))

    for i in tqdm(
        range(len(grid_points)), desc="Building interpolation matrix", unit="lines"
    ):
        triangle_corners = triangulation.simplices[triangles_containing_gridpoints[i]]
        barycentric_coords = triangulation.transform[
            triangles_containing_gridpoints[i], :2
        ].dot(
            grid_points[i]
            - triangulation.transform[triangles_containing_gridpoints[i], 2]
        )
        barycentric_coords = np.append(
            barycentric_coords, 1 - np.sum(barycentric_coords)
        )

        if triangles_containing_gridpoints[i] == -1:
            for j in range(3):
                interpolation_matrix[i, triangle_corners[j]] = np.nan
        else:
            for j in range(3):
                interpolation_matrix[i, triangle_corners[j]] = barycentric_coords[j]

    interpolation_matrix = csr_matrix(interpolation_matrix)

    return interpolation_matrix


def interpolate(
    fast_movie: FastMovie,
    offset=0.0,
    phase_mismatch=0.0,
    shape=(0.1, 2.0 / 3.0, 1.0 / 3.0),
    pixels=0,
    Bezier_points=1000,
    drift_y=None,
    drift_x=None,
    drift_cut="greatest_common",
    method="linear",
    image_range=None,
):
    """Interpolates the pixels in a FAST movie using the analytic positions of the probe.
    Currently only available for interlaced movies.

    Args:
        fast_movie: FastMovie object
        offset: y offset of interpolation points; defaults to 0.0
        phase_mismatch: mismatch of x and y phase; defaults to 0.0; -0.5 is suitable for files before LabView FAST v.???
        shape: 3-tuple describing the shape of the creep in y direction; see wiki for further information
        pixels: excess pixels at top/bottom in up/down frames that have no equvilant in the respective other direction due to creep; defaults to 0
        Bezier_points: number of grid points for the numeric creep function
        drift_y: array of polynomial coefficients defining the drift in y direction
        drift_x: array of polynomial coefficients defining the drift in x direction
        drift_cut: how the frames are cut out of the drift corrected movie:
            'greatest_common' (default): only shows the region which is present in the entire image_range
            'full': does not cut anything off at the edge, so that no information is lost; regions which were not measured are filled with 0
            'size_conserving': does not rescale x and y axis; frames only get shifted, but not distorted
        method: interpolation method; defaults to 'linear', also supports 'cubic'
        image_range: range of images to be interpolated

    Returns:
        nothing
    """

    if method == "lin_fast" and fast_movie.channels != "udi":
        raise ValueError("lin_fast is currently only available for 'udi'")

    if "i" not in fast_movie.channels:
        raise ValueError("Interpolation currently only available for interlacing")

    if fast_movie.mode != "movie":
        raise ValueError("you must first reshape your data in movie mode.")

    if image_range is None:
        image_range = fast_movie.full_image_range

    if isinstance(image_range, int):
        image_range = (image_range,)

    fast_movie.processing_log.info(
        "Performing `{}` 2D grid interpolation in image range {}.".format(
            method, image_range
        )
    )
    fast_movie.processing_log.info(
        "Grid shift: offset = {:05.4f}, phase_mismatch = {:05.4f}.".format(
            offset, phase_mismatch
        )
    )
    fast_movie.processing_log.info(
        "Creep parameters: shape = ({:05.4f}, {:05.4f}, {:05.4f}), pixels = {}, Bezier_points = {}.".format(
            shape[0], shape[1], shape[2], pixels, Bezier_points
        )
    )
    fast_movie.processing_log.info(
        "Polynomial coefficients for y drift: {}".format(drift_y)
    )
    fast_movie.processing_log.info(
        "Polynomial coefficients for x drift: {}".format(drift_x)
    )
    fast_movie.processing_log.info("Drift cutoff method: {}".format(drift_cut))

    nx = fast_movie.data.shape[2]
    ny = fast_movie.data.shape[1]

    # meshgrids
    y, t1 = _output_y_grid(
        ny, nx
    )  # Computing only the grids which are actually need might be more efficient, but this does not seem to be a bottleneck
    x, t2 = _output_x_grid(
        ny, nx
    )  # Leaving the general structure this way to make it easier to adapt to other types of grids

    # correct creep in y direction
    y_up, y_down = _Bezier(y, shape, pixels, Bezier_points)

    # reshape interpolation points to the form required by scipy.interpolate.griddata()
    points_up = np.array([y_up.flatten(), x.flatten()]).T
    points_down = np.array([y_down.flatten(), x.flatten()]).T

    # drift correction
    if "ud" in fast_movie.channels:
        first_frame = image_range[0] * 2
        last_frame = image_range[1] * 2 + 2
        drift_path_image = np.arange(image_range[0], image_range[1] + 1, 0.5)
    else:
        first_frame = image_range[0]
        last_frame = image_range[1] + 1
        drift_path_image = np.arange(image_range[0], image_range[1] + 1, 1.0)
    drift_path_y = np.zeros(last_frame)
    drift_path_x = np.zeros(last_frame)
    if type(drift_y) is list or type(drift_y) is tuple:
        drift_y = np.array(drift_y)
        drift_x = np.array(drift_x)
    if type(drift_y) is np.ndarray:
        deg = drift_y.shape[0] - 1
        for i in range(deg + 1):
            drift_path_y[first_frame:] += drift_y[deg - i] * drift_path_image ** i
            drift_path_x[first_frame:] += drift_x[deg - i] * drift_path_image ** i

    drift_cut_y = np.max(drift_path_y[first_frame:]) - np.min(
        drift_path_y[first_frame:]
    )
    drift_cut_x = np.max(drift_path_x[first_frame:]) - np.min(
        drift_path_x[first_frame:]
    )

    drift_mid_y = (
        np.max(drift_path_y[first_frame:]) + np.min(drift_path_y[first_frame:])
    ) * 0.5
    drift_mid_x = (
        np.max(drift_path_x[first_frame:]) + np.min(drift_path_x[first_frame:])
    ) * 0.5

    # meshgrid of equidistant interpolation points
    if drift_cut == "greatest_common":
        fast_movie.dist_x = (nx - drift_cut_x) / nx
        fast_movie.dist_y = (ny - pixels - drift_cut_y) / ny
        # xnew, ynew = np.meshgrid(t2 * (nx - drift_cut_x) / nx,
        #                         t1 * (ny - pixels - drift_cut_y) / ny)
    elif drift_cut == "full":
        fast_movie.dist_x = (nx + drift_cut_x) / nx
        fast_movie.dist_y = (ny - pixels + drift_cut_y) / ny
        # xnew, ynew = np.meshgrid(t2 * (nx + drift_cut_x) / nx,
        #                         t1 * (ny - pixels + drift_cut_y) / ny)
    elif drift_cut == "size_conserving":
        fast_movie.dist_x = 1.0
        fast_movie.dist_y = (ny - pixels) / ny
        # xnew, ynew = np.meshgrid(t2, t1 * (ny - pixels) / ny)

    xnew, ynew = np.meshgrid(t2 * fast_movie.dist_x, t1 * fast_movie.dist_y)

    ynew += offset

    if method == "lin_fast":

        points_up = list(zip(y_up.flatten(), x.flatten()))
        points_down = list(zip(y_down.flatten(), x.flatten()))
        grid_points = list(zip(ynew.flatten() + phase_mismatch, xnew.flatten()))

        interpolation_matrix_up = get_interpolation_matrix(points_up, grid_points)
        interpolation_matrix_down = get_interpolation_matrix(points_down, grid_points)

        for _, _, frame in tqdm(
            fast_movie.iter_frames(image_range=image_range),
            desc="Interpolation",
            unit="frames",
        ):
            if frame % 2 == 0:
                fast_movie.data[frame] = interpolation_matrix_up.dot(
                    fast_movie.data[frame].flatten()
                ).reshape(ny, nx)
            else:
                fast_movie.data[frame] = interpolation_matrix_down.dot(
                    fast_movie.data[frame].flatten()
                ).reshape(ny, nx)

    else:
        for _, _, frame in tqdm(
            fast_movie.iter_frames(image_range=image_range),
            desc="Interpolation",
            unit="frames",
        ):
            if fast_movie.channels == "udi":
                if frame % 2 == 0:
                    fast_movie.data[frame] = griddata(
                        points_up,
                        fast_movie.data[frame].flatten(),
                        (
                            ynew + phase_mismatch - drift_mid_y + drift_path_y[frame],
                            xnew - drift_mid_x + drift_path_x[frame],
                        ),
                        method=method,
                    ).reshape(ny, nx)
                else:
                    fast_movie.data[frame] = griddata(
                        points_down,
                        fast_movie.data[frame].flatten(),
                        (
                            ynew + phase_mismatch - drift_mid_y + drift_path_y[frame],
                            xnew - drift_mid_x + drift_path_x[frame],
                        ),
                        method=method,
                    ).reshape(ny, nx)
            elif fast_movie.channels == "ui":
                fast_movie.data[frame] = griddata(
                    points_up,
                    fast_movie.data[frame].flatten(),
                    (
                        ynew + phase_mismatch - drift_mid_y + drift_path_y[frame],
                        xnew - drift_mid_x + drift_path_x[frame],
                    ),
                    method=method,
                ).reshape(ny, nx)
            elif fast_movie.channels == "di":
                fast_movie.data[frame] = griddata(
                    points_down,
                    fast_movie.data[frame].flatten(),
                    (
                        ynew + phase_mismatch - drift_mid_y + drift_path_y[frame],
                        xnew - drift_mid_x + drift_path_x[frame],
                    ),
                    method=method,
                ).reshape(ny, nx)
            if drift_cut == "greatest_common" or (drift_y is None and drift_x is None):
                for i, point in enumerate(fast_movie.data[frame, 0, :]):
                    if math.isnan(point):
                        fast_movie.data[frame, 0, i] = fast_movie.data[frame, 1, i]
                for i, point in enumerate(fast_movie.data[frame, -1, :]):
                    if math.isnan(point):
                        fast_movie.data[frame, -1, i] = fast_movie.data[frame, -2, i]

    fast_movie.data = np.nan_to_num(fast_movie.data)


def fit_drift(
    fast_movie: FastMovie,
    deg=1,
    points=None,
    shape=(0.1, 2.0 / 3.0, 1.0 / 3.0),
    pixels=0,
    Bezier_points=1000,
):
    """Fits polynomials to represent the drift in y and x direction.

    Args:
        fast_movie: FastMovie object
        deg: polynomial degree; defaults to 1 (linear fit)
        points: 1D list of image indices which will be used as fitting points; defaults to first and last image
        shape: 3-tuple describing the shape of the creep in y direction; see wiki for further information
        pixels: excess pixels at top/bottom in up/down frames that have no equvilant in the respective other direction due to creep; defaults to 0
        Bezier_points: number of grid points for the numeric creep function

    Returns:
        (tuple): fit information
            - ``drift``: array of drift values in pixels in y and x direction in the given images, with respect to points[0] (which means that drift[0,:] is always [0, 0])
            - ``manipulated_frames``: array of interpolated frames for plotting purposes. in 'udi' mode, only returns 'u' frames
            - ``fit_y``: array of polynomial coefficients defining the drift in y direction
            - ``fit_x``: array of polynomial coefficients defining the drift in x direction

    """

    if "i" not in fast_movie.channels:
        raise ValueError("Interpolation currently only available for interlacing")

    if fast_movie.mode != "movie":
        raise ValueError("you must first reshape your data in movie mode.")

    nx = fast_movie.data.shape[2]
    ny = fast_movie.data.shape[1]

    if points is None:
        points = np.array([0, -1])
    else:
        points = np.array(points)

    if points[-1] == -1:
        points[-1] = fast_movie.num_images - 1

    fast_movie.processing_log.info(
        "Fitting drift correction at images {} with polynomial degree {}.".format(
            points, deg
        )
    )
    fast_movie.processing_log.info(
        "Creep parameters: shape = ({:05.4f}, {:05.4f}, {:05.4f}), pixels = {}, Bezier_points = {}.".format(
            shape[0], shape[1], shape[2], pixels, Bezier_points
        )
    )
    fast_movie.processing_log.info(
        "This will interpolate several frames, which will be restored to their original form afterwards; the data array will be unchanged after fitting."
    )

    if "ud" in fast_movie.channels:
        stashed_frames = np.array(
            [
                [
                    copy(fast_movie.data[2 * ind, :, :]),
                    copy(fast_movie.data[2 * ind + 1, :, :]),
                ]
                for ind in points
            ]
        )
    else:
        stashed_frames = np.array([copy(fast_movie.data[ind, :, :]) for ind in points])

    drift = np.zeros((points.shape[0], 2))

    interpolate(
        fast_movie,
        shape=shape,
        pixels=pixels,
        Bezier_points=Bezier_points,
        image_range=[points[0], points[0]],
    )

    ind_prev = points[0]

    for i, ind in enumerate(points[1:]):
        interpolate(
            fast_movie,
            shape=shape,
            pixels=pixels,
            Bezier_points=Bezier_points,
            image_range=[ind, ind],
        )

        if "ud" in fast_movie.channels:
            corr = correlate(
                fast_movie.data[ind * 2], fast_movie.data[ind_prev * 2], "same", "fft"
            )
        else:
            corr = correlate(
                fast_movie.data[ind], fast_movie.data[ind_prev], "same", "fft"
            )

        drift[i + 1, :] = (
            np.unravel_index(np.argmax(corr), (ny, nx))
            - np.array([ny / 2, nx / 2])
            + drift[i, :]
        )
        ind_prev = ind

    fit_y = np.polyfit(points, drift[:, 0], deg)
    fit_x = np.polyfit(points, drift[:, 1], deg)

    if "ud" in fast_movie.channels:
        manipulated_frames = np.array(
            [copy(fast_movie.data[2 * ind, :, :]) for ind in points]
        )
        for i, ind in enumerate(points):
            fast_movie.data[2 * ind, :, :] = stashed_frames[i, 0, :, :]
            fast_movie.data[2 * ind + 1, :, :] = stashed_frames[i, 1, :, :]
    else:
        manipulated_frames = np.array(
            [copy(fast_movie.data[ind, :, :]) for ind in points]
        )
        for i, ind in enumerate(points):
            fast_movie.data[ind, :, :] = stashed_frames[i, :, :]

    fast_movie.processing_log.info(
        "Estimated polynomial coefficients for y drift: {}".format(fit_y)
    )
    fast_movie.processing_log.info(
        "Estimated polynomial coefficients for x drift: {}".format(fit_x)
    )

    return drift, manipulated_frames, fit_y, fit_x
