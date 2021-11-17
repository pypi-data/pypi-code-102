import numpy as np

import npx


def test_unique_tol():
    a = [0.1, 0.15, 0.7]

    a_unique = npx.unique(a, 2.0e-1)
    print(a_unique)
    assert np.all(a_unique == [0.1, 0.7])

    a_unique, inv = npx.unique(a, 2.0e-1, return_inverse=True)
    assert np.all(a_unique == [0.1, 0.7])
    assert np.all(inv == [0, 0, 1])
