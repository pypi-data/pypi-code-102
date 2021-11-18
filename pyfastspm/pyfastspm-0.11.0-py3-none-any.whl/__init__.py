import logging

from .analysis.analysis import pixel_trace

# convenience imports
from .fast_movie import FastMovie
from .filters_1D.fft import (
    convert_to_spectrum,
    convert_to_timeseries,
    filter_freq,
    filter_noise,
    show_fft,
)
from .filters_2D.baseline import baseline_corr, plane_2D, plot_baseline
from .filters_2D.conv_mat import conv_mat
from .filters_2D.decos import accurate_decos, quick_decos
from .filters_2D.half_pixel_correct import correct_half_pixel_drift
from .filters_2D.interpolate import fit_creep, fit_drift, interpolate
from .tools.file_tools import h5_files_in_folder, preview_folder, unprocessed_in_folder
from .version import __version__


class NullHandler(logging.Handler):
    def emit(self, record):
        pass


logging.getLogger(__name__).addHandler(NullHandler())
__FORMAT = "%(levelname)s[%(module)s.%(funcName)s]:  %(message)s"
logging.basicConfig(level=logging.INFO, format=__FORMAT)
logging.raiseExceptions = True

logging.info("Loaded pyfastspm v" + __version__)

del NullHandler
