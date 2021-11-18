from geodome.tessellation import *
from geodome.neighbourhood_search import *

import numpy as np

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class NormaliseLengthTest(unittest.TestCase):
    def test_normalise(self):
        normalised = normalise_length.py_func(np.array([4, 4, 4], dtype=np.float64))
        self.assertEqual(0.58, round(normalised[0], 2))

    def test_normalise_different_numbers(self):
        normalised = normalise_length.py_func(np.array([4, 7, 6], dtype=np.float64))
        self.assertEqual(0.40, round(normalised[0], 2))
        self.assertEqual(0.70, round(normalised[1], 2))
        self.assertEqual(0.60, round(normalised[2], 2))
