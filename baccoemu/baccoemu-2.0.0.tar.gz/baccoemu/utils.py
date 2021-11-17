import numpy as np
import copy
import pickle
import progressbar
import hashlib
from ._version import __version__

def _md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def _transform_space(x, space_rotation=False, rotation=None, bounds=None):
    """Normalize coordinates to [0,1] intervals and if necessary apply a rotation

    :param x: coordinates in parameter space
    :type x: ndarray
    :param space_rotation: whether to apply the rotation matrix defined through
                           the rotation keyword, defaults to False
    :type space_rotation: bool, optional
    :param rotation: rotation matrix, defaults to None
    :type rotation: ndarray, optional
    :param bounds: ranges within which the emulator hypervolume is defined,
                   defaults to None
    :type bounds: ndarray, optional
    :return: normalized and (if required) rotated coordinates
    :rtype: ndarray
    """
    if space_rotation:
        #Get x into the eigenbasis
        R = rotation['rotation_matrix'].T
        xR = copy.deepcopy(np.array([np.dot(R, xi)
                                     for xi in x]))
        xR = xR - rotation['rot_points_means']
        xR = xR/rotation['rot_points_stddevs']
        return xR
    else:
        return (x - bounds[:, 0])/(bounds[:, 1] - bounds[:, 0])


def _bacco_evaluate_emulator(emulator, coordinates, gp_name='gpy', values=None, sample=False):
    """
    Function evaluating the emulator at some given points.

    :param emulator: the trained gaussian process
    :type emulator: obj
    :param coordinates: points where to predict the function
    :type coordinates: array-like
    :param gp_name: type of gaussian process code to use; options are 'gpy',
                    'george' and 'sklearn', defaults to 'gpy'
    :type gp_name: str
    :param values: only for 'george', the original evaluations of the gp at the
                   coordinates used for training, defaults to None.
    :type values: array-like
    :param sample: only for 'george', whether to take only one sample of the
                   prediction or the full prediction with its variance; if
                   False, returns the full prediction, defaults to False
    :type sample: bool

    :returns: emulated values and variance of the emulation.
    :rtype: float or array_like
    """

    if gp_name == 'gpy':
        deepGP = False
        if deepGP is True:
            res = emulator.predict(coordinates)
            evalues, cov = (res[0].T)[0], (res[1].T)[0]
        else:
            res = emulator.predict(coordinates)
            evalues, cov = (res[0].T)[0], (res[1].T)[0]
    elif gp_name == 'sklearn':
        evalues, cov = emulator.predict(coordinates, return_cov=True)
    elif gp_name == 'george':
        if sample:
            evalues = emulator.predict(values, coordinates)
            cov = 0
        else:
            #import ipdb; ipdb.set_trace()
            # (coordinates,mean_only=False)
            evalues, cov = emulator.predict(
                values, coordinates, return_var=True)
    else:
        raise ValueError('emulator type {} not valid'.format(gp_name))

    return evalues, np.abs(cov)


class MyProgressBar():
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar=progressbar.ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()
