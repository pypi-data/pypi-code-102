'''
Copyright (C) 2021, Alejandro Cardenas-Avendano, Alex Lupsasca & Hengrui Zhu
This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with this program. 
If not, see https://www.gnu.org/licenses/.
'''
import numpy as np
import matplotlib.pyplot as plt
import sys
import warnings
import h5py

#For the analytical calculations
from numpy.lib.scimath import sqrt
from numpy import arccos, arcsin
from scipy.special import ellipk, ellipeinc, ellipe
from scipy.special import ellipkinc as ellipf
from scipy.special import ellipj
from scipy.integrate import cumtrapz,quad

#Required for the wrapper for elliptic integral of the third kind
import ctypes
import numpy.ctypeslib as ctl

#For the lensing bands
from scipy.spatial import Delaunay

#Radon transformation
from skimage.transform import radon

from scipy.interpolate import griddata
from scipy.interpolate import LinearNDInterpolator
from scipy.interpolate import RegularGridInterpolator
from scipy.optimize import curve_fit
from scipy.fft import fft, fftfreq, fftshift
from scipy import interpolate, optimize 

#Plotting 
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid1 import make_axes_locatable
cmap = plt.get_cmap('afmhot') # This is the official colors of the BHs!

#M
import misc as ms

#Warnings flags
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)
warnings.simplefilter("ignore", UserWarning)