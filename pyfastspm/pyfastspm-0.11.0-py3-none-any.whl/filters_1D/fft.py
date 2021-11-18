"""1D filters to be performed on the timeseries before it is reshaped to a movie."""

import logging

import matplotlib.pyplot as plt
import mkl_fft
import numpy as np
import scipy
from scipy import interpolate

from ..fast_movie import FastMovie

log = logging.getLogger(__name__)


def convert_to_spectrum(fast_movie: FastMovie):
    """Converts a FastMovie object from 'timeseries' mode to 'spectrum' mode using fft.

    Args:
        fast_movie: FastMovie object

    Returns:
        Nothing

    """
    if not fast_movie.mode == "timeseries":
        if fast_movie.mode == "movie":
            raise ValueError(
                "1D corrections have to be applied before reshaping to movie."
            )
        if fast_movie.mode == "spectrum":
            raise ValueError("FastMovie object is already in spectrum mode.")
        else:
            raise ValueError("FastMovie object has to be in timeseries mode.")

    try:
        fast_movie.data = mkl_fft.rfft(fast_movie.data)
    except ValueError:
        fast_movie.processing_log.warning("falling back to numpy rfft.")
        log.warning("falling back to numpy rfft.")
        fast_movie.data = np.fft.rfft(fast_movie.data)

    fast_movie.mode = "spectrum"

    fast_movie.processing_log.info("converted to spectrum mode.")


def convert_to_timeseries(fast_movie: FastMovie):
    """Converts a FastMovie object from 'spectrum' mode to 'timeseries' mode using inverse fft.

    Args:
        fast_movie: FastMovie object

    Returns:
        Nothing

    """
    if not fast_movie.mode == "spectrum":
        if fast_movie.mode == "movie":
            raise ValueError(
                "1D corrections have to be applied before reshaping to movie."
            )
        if fast_movie.mode == "timeseries":
            raise ValueError("FastMovie object is already in timeseries mode.")
        else:
            raise ValueError("FastMovie object has to be in spectrum mode.")

    try:
        fast_movie.data = mkl_fft.irfft(fast_movie.data)
    except (ValueError, TypeError):
        fast_movie.processing_log.warning("falling back to numpy irfft.")
        log.warning("falling back to numpy irfft.")
        fast_movie.data = np.fft.irfft(fast_movie.data)

    fast_movie.mode = "timeseries"

    fast_movie.processing_log.info("converted to timeseries mode.")


def show_fft(fast_movie: FastMovie, range_display=None, filename=None):
    """Displays the real part of the data of a FastMovie object in 'spectrum' mode.

    Args:
        fast_movie: FastMovie object
        range_display: 2 element list specifying the range in Hz to be displayed.
            Defaults to entire spectrum.
        filename: if given, saves the spectrum to a file with the specified name.
            Otherwise shows it on screen.

    Returns:
        Nothing

    """
    if not fast_movie.mode == "spectrum":
        raise ValueError("Data has to be converted to spectrum first.")

    rate = fast_movie.metadata["Acquisition.ADC_SamplingRate"]

    freq = np.fft.rfftfreq(len(fast_movie.data) * 2 - 1, 1.0 / rate)

    if range_display is not None:
        xmin = int(len(freq) * range_display[0] / freq[-1])
        xmax = int(len(freq) * range_display[1] / freq[-1])
        plt.plot(freq[xmin:xmax], fast_movie.data[xmin:xmax])
    else:
        plt.plot(freq, fast_movie.data)

    plt.xlabel(r"$f\,\mathrm{\,in\,Hz}$")
    plt.tight_layout()

    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)


def filter_freq(fast_movie: FastMovie, freqs, pars, types):
    """Applies multiple filters to a FastMovie object in 'spectrum' mode.

    Args:
        fast_movie: FastMovie object
        freqs: List of filter frequencies
        pars: List of sigmas for Gaussians / error functions
        types: List of filter types. Allowed types are:
            'g': Gaussian filter. Eliminates the filter frequency.
            'h', 'l': High/Low pass filter using an error function.

    Returns:
        Nothing

    """
    if not fast_movie.mode == "spectrum":
        raise ValueError("Data has to be converted to spectrum first.")

    rate = fast_movie.metadata["Acquisition.ADC_SamplingRate"]

    freq = np.fft.rfftfreq(len(fast_movie.data) * 2 - 1, 1.0 / rate)

    for i, filter_freq in enumerate(freqs):
        if types[i] == "g":
            freq_filter = 1.0 - np.exp(-0.5 * ((freq - filter_freq) / pars[i]) ** 2)
            fast_movie.processing_log.info(
                "Prepared frequency elimination filter at {:05.4f} Hz with broadness {:05.4f} Hz.".format(
                    filter_freq, pars[i]
                )
            )
        elif types[i] == "h":
            freq_filter = 0.5 + 0.5 * scipy.special.erf(
                (freq - filter_freq) / np.sqrt(2 * pars[i] ** 2)
            )
            fast_movie.processing_log.info(
                "Prepared high pass filter at {:05.4f} Hz with broadness {:05.4f} Hz.".format(
                    filter_freq, pars[i]
                )
            )
        elif types[i] == "l":
            freq_filter = 0.5 - 0.5 * scipy.special.erf(
                (freq - filter_freq) / np.sqrt(2 * pars[i] ** 2)
            )
            fast_movie.processing_log.info(
                "Prepared low pass filter at {:05.4f} Hz with broadness {:05.4f} Hz.".format(
                    filter_freq, pars[i]
                )
            )
        else:
            raise ValueError("Type must be 'g', 'h' or 'l' ")

        fast_movie.data *= freq_filter

    fast_movie.processing_log.info("Frequency filter applied.")


def filter_noise(fast_movie: FastMovie, thresh, sigma, freqs=None):
    """Applies a noise filter to a FastMovie object in 'spectrum' mode.
    If arguments except the first are given as lists, creates a frequency dependent noise filter using spline interpolation.

    Args:
        fast_movie: FastMovie object
        thresh: Noise threshold or list thereof
        sigma: Sigma parameter for error function or list thereof
        freqs: List of frequencies. Only required when using interpolation.

    Returns:
        Nothing

    Warning:

        What this does is essentially time averaging! Noise filters can thus:

        - Reduce noise
        - Enhance contrast
        - Remove streaks

        ... but can also:

        - Add noise
        - Mess up time resolution (averaging over multiple frames)

        Comparison with a version without noise filtering is highly recommended.
        If jumping features leave behind a 'shadow' or do not jump at all, you filtered too much.

        Filters with ``mu`` and ``sigma`` both around the noise level seem to work fairly well

    """
    if not fast_movie.mode == "spectrum":
        raise ValueError("Data have to be converted to spectrum first.")

    if type(thresh) is list:
        rate = fast_movie.metadata["Acquisition.ADC_SamplingRate"]
        freq = np.fft.rfftfreq(len(fast_movie.data) * 2 - 1, 1.0 / rate)

        spline = interpolate.splrep(freqs, thresh, s=0)
        envelope = interpolate.splev(freq, spline)

        spline_sig = interpolate.splrep(freqs, sigma, s=0)
        env_sig = interpolate.splev(freq, spline_sig)

        freq_filter = 0.5 + 0.5 * scipy.special.erf(
            (np.abs(fast_movie.data) - envelope) / np.sqrt(2 * env_sig ** 2)
        )

        fast_movie.processing_log.info(
            "noise filter with thresholds {} and sigmas {} at frequencies {} applied to {}".format(
                thresh, sigma, freqs, fast_movie
            )
        )
    else:
        freq_filter = 0.5 + 0.5 * scipy.special.erf(
            (np.abs(fast_movie.data) - thresh) / np.sqrt(2 * sigma ** 2)
        )
        fast_movie.processing_log.info(
            "noise filter with threshold {:05.4f} and sigma {:05.4f} applied".format(
                thresh, sigma
            )
        )

    fast_movie.data *= freq_filter

    log.warning(
        "what this does is essentially time averaging! Comparison with "
        "a version without noise filtering is highly recommended."
    )
