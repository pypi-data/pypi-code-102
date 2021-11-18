from typing import List, Dict, Tuple, Union

import numpy as np
import scipy.stats as st
from mysutils.collections import merge_dicts


def confidence_score(measures: Union[List[Dict[str, float]], Dict[str, List[float]]],
                     ci: float = 0.95) -> Dict[str, Tuple[float, float]]:
    """ Obtain the mean value and confidence interval for a list of measures for different metrics.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :param ci: The coefficient interval threshold in a value between 0 and 1.
    :return: A dictionary with the different metrics and a tuple with the mean value and the confidence interval.
    """
    measures = merge_dicts(measures) if isinstance(measures, List) else measures
    intervals = {key: st.t.interval(ci, len(v) - 1, loc=np.mean(v), scale=st.sem(v)) for key, v in measures.items()}
    return {key: ((b + a) / 2, (b - a) / 2) for key, (a, b) in intervals.items()}


def measures_mean(measures: Union[List[Dict[str, float]], Dict[str, List[float]]]) -> Dict[str, float]:
    """ Obtain the mean value of a list of measures for different metrics.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :return: A dictionary with the different metrics and the mean value of each metric.
    """
    measures = merge_dicts(measures) if isinstance(measures, List) else measures
    return {key: np.mean(values) for key, values in measures.items()}


def standard_deviation(measures: Union[List[Dict[str, float]], Dict[str, List[float]]]) -> Dict[str, float]:
    """ Obtain the standard deviation of a list of measures for different metrics.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :return: A dictionary with the different metrics and the standard deviation of each metric.
    """
    measures = merge_dicts(measures) if isinstance(measures, List) else measures
    return {key: np.std(values) for key, values in measures.items()}


def standard_error(measures: Union[List[Dict[str, float]], Dict[str, List[float]]]) -> Dict[str, float]:
    """ Obtain the standard error of a list of measures for different metrics.

    :param measures: A list of measures or a dictionary with different metrics and a vector of values for each metric.
    :return: A dictionary with the different metrics and the standard error of each metric.
    """
    measures = merge_dicts(measures) if isinstance(measures, List) else measures
    return {key: np.std(values) / len(values) for key, values in measures.items()}
