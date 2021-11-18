"""
Contains all the functions required to handle color mapping of the frames
"""
import logging

import matplotlib.cm as cm
import matplotlib.colors as mplc
import numpy as np
from scipy.ndimage.interpolation import zoom

log = logging.getLogger(__name__)


def gray_to_rgb(
    data, color_map="hot", contrast=None, scaling=(1.0, 1.0), interp_order=3
):
    """

    Converts a single-channel image to an RGB image by applying a ``matplotlib`` color_map
    and normalizing the contrast to a given range.

    Args:
        data: input 2darray data
        color_map: one of the standard ``matplotlib`` colormaps
        contrast: a float between 0 and 1, a sequence of two floats between 0 and 1,
            or a sequence of two integers.
        scaling: 2 element list defining the scaling in both directions to be applied to the image. Defaults to no scaling (1.0, 1.0)
        interp_order: an integer in the 0-5 range indicating the interpolation order of the scaling.
                For more information see the `scipy.nd.zoom documentation
                <https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.zoom.html#scipy.ndimage.zoom>`_

    Returns:
        a ndarray of RGB data. RGB values range in 0...255

    Notes:
        See the documentation of the ``get_contrast_limits`` function for more details on the ``contrast`` parameter

    """
    if data.ndim != 2:
        raise ValueError("Dimension of input array is not 2.")
    value_levels = get_contrast_limits(data, contrast=contrast)
    if any(i != 1.0 for i in scaling):
        data = zoom(data, scaling, order=interp_order)
    norm = mplc.Normalize(vmin=value_levels[0], vmax=value_levels[1])
    mappable = cm.ScalarMappable(norm=norm, cmap=color_map)
    return (mappable.to_rgba(data)[:, :, 0:3] * 255).astype(np.uint8)


def get_contrast_limits(data, contrast=None):
    """Calculates the minimum and maximum values where to cut the data range according to the specified contrast range.

    Args:
        data: a single 2darray or a 1darray of 2darrays
        contrast: (optional) tuple of two ints, tuple of two floats between 0 and 1, float between 0 and 1.
            Defaults to full contrast range.

    Returns: a tuple of two ints representing the min and max values

    Notes:
        More specifically the ``contrast`` parameter can be conveniently specified as:

            * a float between 0 and 1, which is interpreted as the fraction of the image histogram
              to be **kept** in the contrast range (default)
            * a sequence of two floats between 0 and 1, indicating the fractions of the image histogram
              to be **discarded** in the contrast, at the bottom and at the top of the image range, respectively
            * a sequence of two integers is interpreted as a *manual* setting of the contrast,
              where the values correspond
              to the minimum and maximum value of the data
    """
    contrast = np.array(contrast) if contrast is not None else None
    if contrast is None:
        p1, p2 = int(data.min()), int(data.max())
    elif np.issubclass_(contrast.dtype.type, np.floating):
        if contrast.size == 1 and 0 <= contrast <= 1:
            limits = (100.0 * (1 - contrast) / 2, 100.0 * (1 - (1 - contrast) / 2))
        elif contrast.size == 2 and 0 <= contrast[0] <= 1 and 0 <= contrast[1] <= 1:
            limits = (100.0 * contrast[0], 100.0 * contrast[1])
        else:
            raise ValueError(
                "'contrast' must be a float, a tuple of two floats between 0 and 1, or a tuple of two ints."
            )
        p1, p2 = np.percentile(data, (limits[0], limits[1]))
        log.debug("Auto-set contrast limits are {0:g} and {1:g}".format(p1, p2))

    elif np.issubclass_(contrast.dtype.type, np.integer):
        if contrast.size != 2:
            raise ValueError("'contrast' must be a sequence of two ints (or floats).")
        if contrast[0] >= contrast[1]:
            raise ValueError(
                "Lower bound of contrast must be smaller than the higher bound."
            )
        p1, p2 = contrast[0], contrast[1]
        log.debug("Manual contrast limits are {0:g} and {1:g}".format(p1, p2))

    else:
        raise ValueError(
            "'contrast' must be a float, a tuple of two floats between 0 and 1, or a tuple of two ints."
        )
    return (int(p1), int(p2))
