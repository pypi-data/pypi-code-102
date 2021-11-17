# -*- coding: utf-8 -*-
"""
Created on June 18 06:54:04 2021
GUI routine for Laue neural network training and prediction

@author: Ravi raj purohit PURUSHOTTAM RAJ PUROHIT (purushot@esrf.fr)
@guide: jean-Sebastien MICHA (micha@esrf.fr)

Lattice and symmetry routines are extracted and modified from the PYMICRO repository

TODO:
    1. HDF5 file format output instead of pickle
    2. Notebook to post process the results (choice of bin width, data selectivity, etc...)
    3. Hexagonal system problem still not resolved !!!!! (go to previous ORIX approach)
    4. Multi processing variables ?
    5. Remove ORIX dependecy if possible, but IPF would be easier!!
"""
try:
    import pkg_resources  # part of setuptools
    version_package = pkg_resources.require("lauetoolsnn")[0].version
except:
    version_package = "3.0.0"

frame_title = "Laue Neural-Network model- v3 @Ravi @Jean-Sebastien \n@author: Ravi raj purohit PURUSHOTTAM RAJ PUROHIT (purushot@esrf.fr) \n@guide: Jean-Sebastien MICHA (micha@esrf.fr)"

import warnings
warnings.filterwarnings('ignore')
import logging
logger = logging.getLogger()
old_level = logger.level
logger.setLevel(100)

import matplotlib
matplotlib.use('Qt5Agg')
matplotlib.rcParams.update({'font.size': 14})
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import numpy as np
import os
import collections
import random, itertools
import re
import glob
import _pickle as cPickle
import time, datetime
import sys
import inspect
import threading
import multiprocessing as multip
# import ctypes as c_type
from multiprocessing import Process, Queue, cpu_count
import ast, configparser
from sklearn.metrics import classification_report

from PyQt5 import QtCore#, QtGui
from PyQt5.QtCore import QSettings
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,\
                            QPushButton, QWidget, QFormLayout, \
                            QToolBar, QStatusBar, \
                            QVBoxLayout, QTextEdit, QProgressBar, \
                            QComboBox, QLineEdit, QFileDialog

## LaueTools import
import LaueTools.dict_LaueTools as dictLT
import LaueTools.IOLaueTools as IOLT
import LaueTools.generaltools as GT
# import LaueTools.CrystalParameters as CP
import LaueTools.LaueGeometry as Lgeo
import LaueTools.readmccd as RMCCD
## for faster binning of histogram
## C version of hist
from fast_histogram import histogram1d
## Keras import
tensorflow_keras = True
try:
    import tensorflow as tf
    from tensorflow.keras.callbacks import Callback
    import keras
    from keras.models import model_from_json
    from keras.models import Sequential
    from keras.layers import Dense, Activation, Dropout
    from tensorflow.keras.utils import to_categorical
    from keras.callbacks import EarlyStopping, ModelCheckpoint
    from keras.regularizers import l2
    # from tf.keras.layers.normalization import BatchNormalization
except:
    tensorflow_keras = False

##ORIX library  (to come back later if IPF is resolved in ORIX)
# from diffpy.structure import Lattice as latdiffpy
# from diffpy.structure import Structure as strucdiffpy
# from orix.crystal_map import Phase
# from orix.vector import Miller
# from orix.vector.miller import _round_indices

## util library with MP function
try:
    from utils_lauenn import Symmetry,Lattice,\
        simulatemultiplepatterns, worker_generation, chunker_list,\
            rot_mat_to_euler, read_hdf5, get_ipf_colour,predict_ubmatrix, predict,\
                predict_preprocessMP, global_plots, save_sst, texttstr, get_material_data,\
                    write_training_testing_dataMTEX, SGLattice, _round_indices, simulate_spots
except:
    from lauetoolsnn.utils_lauenn import Symmetry,Lattice,\
        simulatemultiplepatterns, worker_generation, chunker_list,\
            rot_mat_to_euler, read_hdf5, get_ipf_colour,predict_ubmatrix, predict,\
                predict_preprocessMP, global_plots, save_sst, texttstr, get_material_data,\
                    write_training_testing_dataMTEX, SGLattice, _round_indices, simulate_spots
                    
## GPU Nvidia drivers needs to be installed! Ughh
## if wish to use only CPU set the value to -1 else set it to 0 for GPU
## CPU training is suggested (as the model requires more RAM)
try:
    # Disable all GPUS
    tf.config.set_visible_devices([], 'GPU')
    visible_devices = tf.config.get_visible_devices()
    for device in visible_devices:
        assert device.device_type != 'GPU'
except:
    # Invalid device or cannot modify virtual devices once initialized.
    pass
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

Logo = resource_path("lauetoolsnn_logo.png")

default_initialization = True
if default_initialization:
    material_global = "Cu" ## same key as used in LaueTools
    material1_global = "Si" ## same key as used in LaueTools
    symmetry_global = "cubic"
    symmetry1_global = "cubic"
    prefix_global = ""
    detectorparameters_global = [79.583,976.202,931.883,0.4411,0.3921]
    pixelsize_global = 0.0734 # 0.079142 #
    ccd_label_global = "sCMOS" #"MARCCD165" #"Cor"#
    dim1_global = 2018 #2048 #
    dim2_global = 2016 #2048 #
    emax_global = 23
    emin_global = 5
    UB_matrix_global = 5
    image_grid_globalx = 21
    image_grid_globaly = 51
    intensity_threshold_global = 80 #75 800
    boxsize_global = 15
    fit_peaks_gaussian_global = 1
    FitPixelDev_global = 15
    strain_label_global = "NO" ## compute and plot strains
    tolerance_strain = [0.35,0.25,0.15]   ## reduced tolerance for strain calculations
    tolerance_strain1 = [0.35,0.25,0.15]
    hkls_list_global = "[1,1,0],[1,0,0],[1,1,1]"#,[3,1,0],[5,2,9],[7,5,7],[7,5,9]"
    ##exp directory
    if material_global == material1_global:
        fn1 = material_global + prefix_global
    else:
        fn1 = material_global + "_" + material1_global + prefix_global
    expfile_global = r"C:\Users\purushot\Desktop\Tungsten_olivier_data\d0-300MPa"
    exp_prefix_global = "Wmap_WB_13sep_d0_300MPa_" #"nw2_" #None #"roi3_" #
    modelfile_global = r"C:\Users\purushot\Desktop\pattern_matching\experimental\GUIv0\latest_version" + "//" + fn1
    if material_global == material1_global:
        fn1 = material_global
        if exp_prefix_global == None:
            exp_prefix_global = material_global + "_"
        weightfile_global = modelfile_global + "//" + "model_" + material_global + ".h5"
    else:
        fn1  = material_global + "_" + material1_global
        if exp_prefix_global == None:
            exp_prefix_global = material_global + "_"+material1_global + "_"
        weightfile_global = modelfile_global + "//" + "model_" + material_global + "_" + material1_global + ".h5"
    main_directory = os.getcwd()
    hkl_max_global = "5"
    elements_global = "all"
    freq_rmv_global = 100
    hkl_max1_global = "5"
    elements1_global = "all"
    freq_rmv1_global = 100
    maximum_angle_to_search_global = 90
    step_for_binning_global = 0.1
    nb_grains_per_lp_global = 3
    nb_grains_per_lp1_global = 3
    grains_nb_simulate_global = 1000
    include_scm_global = False
    batch_size_global = 50
    epochs_global = 5
    tolerance_global = 0.5
    tolerance_global1 = 0.5
    model_weight_file = None
    softmax_threshold_global = 0.80 # softmax_threshold
    mr_threshold_global = 0.90 # match rate threshold
    cap_matchrate = 0.01 * 100 ## any UB matrix providing MR less than this will be ignored
    coeff = 0.15 ## should be same as cap_matchrate or no?
    coeff_overlap1212 = 0.15
    NumberMaxofFits = 3000 ### Max peaks per LP
    mode_spotCycle = "graphmode" ## slow: to cycle through all spots else: cycles through smartly selected pair of spots
    material0_limit1212 = 100000
    material1_limit1212 = 100000
    use_previous_UBmatrix = False
    write_mtex_file = True
    material0_lauegroup = "11"
    material1_lauegroup = "11"
    misorientation_angle1 = 1
    cpu_count_user = 1

if cpu_count_user == -1:
    cpu_count_user = cpu_count()//2

GUI_START_TIME = time.time() #in ms
metricsNN = [
            keras.metrics.FalseNegatives(name="fn"),
            keras.metrics.FalsePositives(name="fp"),
            keras.metrics.TrueNegatives(name="tn"),
            keras.metrics.TruePositives(name="tp"),
            keras.metrics.Precision(name="precision"),
            keras.metrics.Recall(name="accuracy"),
            ]
ACCEPTABLE_FORMATS = [".npz"]
gui_state = np.random.randint(1e6)
#%% Main module
class Window(QMainWindow):
    """Main Window."""
    def __init__(self, winx=None, winy=None):
        """Initializer."""
        super(Window, self).__init__()
        # QMainWindow.__init__(self)

        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        if winx==None or winy==None:
            self.setFixedSize(16777215,16777215)
        else:
            self.setFixedSize(winx, winy)
        
        self.setWindowTitle("Laue Neural-Network v3")
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        
        ## init variables
        self.input_params = {}
        self.factor = 5 ## fixed for 20% validation dataset generation
        self.state = 0
        self.state1 = 0
        self.state2 = 0
        self.model = None
        self.mode_spotCycleglobal = mode_spotCycle
        self.softmax_threshold_global = softmax_threshold_global
        self.mr_threshold_global = mr_threshold_global
        self.cap_matchrate = cap_matchrate
        self.coeff = coeff
        self.coeff_overlap = coeff_overlap1212
        self.fit_peaks_gaussian_global = fit_peaks_gaussian_global
        self.FitPixelDev_global = FitPixelDev_global
        self.NumberMaxofFits = NumberMaxofFits
        self.tolerance_strain = tolerance_strain
        self.tolerance_strain1 = tolerance_strain1
        self.misorientation_angle = misorientation_angle1
        self.material0_limit = material0_limit1212
        self.material1_limit = material1_limit1212
        self.material_phase_always_present = "none"
        self.use_previous_UBmatrix = use_previous_UBmatrix
        self.crystal = None
        self.SG = None
        self.general_diff_rules = False
        self.crystal1 = None
        self.SG1 = None
        self.general_diff_rules1 = False
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.layout)
        self._createDisplay() ## display screen
        self.setDisplayText("Lauetoolsnn v"+ str(version_package))
        self.setDisplayText(frame_title)
        self.setDisplayText("Uses base libraries of LaueTools (micha@esrf.fr) to simulate Laue patterns for a given detector geometry \nFollows convention of BM32 beamline at ESRF")
        self.setDisplayText("Polefigure and IPF plot modules are taken and modified from PYMICRO repository; HKL multiplicity and conditions are taken from xrayutilities library")
        self.setDisplayText("This version supports multiprocessing \nGUI initialized! \nLog will be printed here \nPlease Train a model first, if not already done.\n")
        self.setDisplayText("New materials and extinction rules can be set in LaueTools DictLP file before launching this module")
        self.setDisplayText("For now the Learning rate of optimizer, Kernel and Bias weight Initializers are already optimized and set in the in-built model (can also be set to different values in the config window)"+\
                            " (TO find another set of parameters please use Hyper parameter optimization routine in GUI)")
        self.setDisplayText("Load a config file first (for example see the example_config tab)")
        self._formLayout() ## buttons and layout
        self.popups = []
        # self.showMaximized()
        self.setFixedSize(16777215,16777215)
        
    def closeEvent(self, event):
        try:
            self.text_file_log.close()
        except:
            print("Nothing to close")
        self.close
        QApplication.closeAllWindows()
        super().closeEvent(event)
        
    def _createDisplay(self):
        """Create the display."""
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.append('%s'%text)
        self.display.moveCursor(QtGui.QTextCursor.End)
        self.display.setFocus()

    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Load Config', self.getfileConfig)
        self.menu.addAction('&Exit', self.close)
    
    def getfileConfig(self):
        filenameConfig = QFileDialog.getOpenFileName(self, 'Select the config text file')
        self.load_config_from_file(filenameConfig[0])
    
    def load_config_from_file(self, configFile):
        global material_global, symmetry_global, material1_global, symmetry1_global
        global prefix_global, main_directory, emin_global, emax_global, ccd_label_global
        global detectorparameters_global, pixelsize_global, dim1_global, dim2_global
        global UB_matrix_global, image_grid_globalx , image_grid_globaly 
        global intensity_threshold_global, boxsize_global, fit_peaks_gaussian_global, FitPixelDev_global
        global strain_label_global, tolerance_strain, tolerance_strain1, hkls_list_global
        global expfile_global, exp_prefix_global, modelfile_global, weightfile_global
        global hkl_max_global, elements_global, freq_rmv_global, hkl_max1_global
        global elements1_global, freq_rmv1_global, maximum_angle_to_search_global
        global step_for_binning_global, nb_grains_per_lp_global, nb_grains_per_lp1_global
        global grains_nb_simulate_global, include_scm_global, batch_size_global, epochs_global
        global tolerance_global, model_weight_file, material0_limit1212, material1_limit1212, tolerance_global1
        global softmax_threshold_global, mr_threshold_global, cap_matchrate, coeff, cpu_count_user
        global coeff_overlap1212, mode_spotCycle, NumberMaxofFits, use_previous_UBmatrix
        global write_mtex_file, material0_lauegroup, material1_lauegroup, misorientation_angle1
        
        config = configparser.ConfigParser()
        
        try:
            config.read_file(open(configFile))
        except:
            self.write_to_console("File not selected, nothing to open")
            return
            
        material_global = config.get('MATERIAL', 'material')
        symmetry_global = config.get('MATERIAL', 'symmetry')
        
        try:
            self.SG = int(config.get('MATERIAL', 'space_group'))
        except:
            if symmetry_global =="cubic":
                self.SG = 230
            elif symmetry_global =="monoclinic":
                self.SG = 10
            elif symmetry_global == "hexagonal":
                self.SG = 191
            elif symmetry_global == "orthorhombic":
                self.SG = 47
            elif symmetry_global == "tetragonal":
                self.SG = 123
            elif symmetry_global == "trigonal":
                self.SG = 162
            elif symmetry_global == "triclinic":
                self.SG = 2
            self.write_to_console("Space group is not defined, by default taking the higher order for the specified symmetry")
        
        try:
            self.general_diff_rules = config.get('MATERIAL', 'general_diffraction_rules') == "true"
        except:
            self.general_diff_rules = False
            self.write_to_console("general_diffraction_rules is not defined, by default False")
        
        try:
            cpu_count_user = int(config.get('CPU', 'n_cpu'))
            if cpu_count_user <= 0 or cpu_count_user > cpu_count():
                cpu_count_user = cpu_count()
        except:
            cpu_count_user = cpu_count()
        
        try:
            material1_global = config.get('MATERIAL', 'material1')
            symmetry1_global = config.get('MATERIAL', 'symmetry1')
            
            try:
                self.SG1 = int(config.get('MATERIAL', 'space_group1'))
            except:
                if symmetry1_global =="cubic":
                    self.SG1 = 230
                elif symmetry1_global =="monoclinic":
                    self.SG1 = 10
                elif symmetry1_global == "hexagonal":
                    self.SG1 = 191
                elif symmetry1_global == "orthorhombic":
                    self.SG1 = 47
                elif symmetry1_global == "tetragonal":
                    self.SG1 = 123
                elif symmetry1_global == "trigonal":
                    self.SG1 = 162
                elif symmetry1_global == "triclinic":
                    self.SG1 = 2
                self.write_to_console("Space group 1 is not defined, by default taking the higher order for the specified symmetry")
                
            try:
                self.general_diff_rules1 = config.get('MATERIAL', 'general_diffraction_rules1') == "true"
            except:
                self.general_diff_rules1 = False
                self.write_to_console("general_diffraction_rules1 is not defined, by default False")
        except:
            material1_global = "none"
            symmetry1_global = "none"
            self.SG1 = "none"
            self.general_diff_rules1 = False
            self.write_to_console("Only one material is defined, by default taking the other one as 'none'")
        
        if material1_global == "none" and symmetry1_global =="none":
            material1_global = material_global
            symmetry1_global = symmetry_global         
        
        prefix_global = str(config.get('GLOBAL_DIRECTORY', 'prefix'))
        main_directory = str(config.get('GLOBAL_DIRECTORY', 'main_directory'))
        
        detectorfile = config.get('DETECTOR', 'detectorfile')
        try:
            emax_global = float(config.get('DETECTOR', 'emax'))
            emin_global = float(config.get('DETECTOR', 'emin'))
        except:
            self.write_to_console("Detector energy range not defined, using default values of 5-23KeV")
            
        try:
            _file = open(detectorfile, "r")
            text = _file.readlines()
            _file.close()
            # first line contains parameters
            parameters = [float(elem) for elem in str(text[0]).split(",")]
            detectorparameters_global = parameters[:5]
            pixelsize_global = parameters[5]
            dim1_global = parameters[6]
            dim2_global = parameters[7]
            # others are comments
            comments = text[1:]
            ccd_label_global = ""
            for line in comments:
                if line.startswith("# CCDLabel"):
                    ccd_label_global = line.split(":")[1].strip()
            if ccd_label_global == "":
                self.write_to_console("CCD label cannot be read from the calibration file, setting it to latest detector sCMOS")
                ccd_label_global = "sCMOS"
        except IOError as error:
            self.write_to_console("Error opening file\n" + str(error))
        except UnicodeDecodeError as error:
            self.write_to_console("Error opening file\n" + str(error))
        
        try:
            UB_matrix_global = int(config.get('PREDICTION', 'UB_matrix_to_detect'))
        except:
            self.write_to_console("UB matrix to identify not defined, can be set in the Prediction window")
        
        try:
            image_grid_globalx = int(config.get('EXPERIMENT', 'image_grid_x'))
            image_grid_globaly = int(config.get('EXPERIMENT', 'image_grid_y'))
        except:
            self.write_to_console("Scan grid not defined, can be set in the Prediction window")
        
        try:
            softmax_threshold_global = float(config.get('PREDICTION', 'softmax_threshold_global'))
        except:
            self.write_to_console("Softmax threshold not defined, using default 80%")
        self.softmax_threshold_global = softmax_threshold_global
        
        try:
            mr_threshold_global = float(config.get('PREDICTION', 'mr_threshold_global'))
        except:
            self.write_to_console("Matching rate threshold not defined, using default 95%")
        self.mr_threshold_global = mr_threshold_global
        
        try:
            coeff = float(config.get('PREDICTION', 'coeff'))
        except:
            self.write_to_console("Coeff Overlap v0 not defined, using default 30%")
        self.coeff=coeff

        try:
            coeff_overlap1212 = float(config.get('PREDICTION', 'coeff_overlap'))
        except:
            self.write_to_console("Coeff Overlap not defined, using default 30%")
        self.coeff_overlap=coeff_overlap1212
        
        try:
            mode_spotCycle = str(config.get('PREDICTION', 'mode_spotCycle'))
        except:
            self.write_to_console("Analysis mode not defined, using default graphmode, can be set in Prediction window")
        self.mode_spotCycleglobal = mode_spotCycle
        
        try:
            material0_limit1212 = int(config.get('PREDICTION', 'material0_limit'))
        except:
            self.write_to_console("Max Nb of UB per material 0 not defined, using default maximum")
        self.material0_limit = material0_limit1212
        
        try:
            material1_limit1212 = int(config.get('PREDICTION', 'material1_limit'))
        except:
            self.write_to_console("Max Nb of UB per material 1 not defined, using default maximum")
        self.material1_limit = material1_limit1212
        
        intensity_threshold_global = float(config.get('PEAKSEARCH', 'intensity_threshold'))
        boxsize_global = int(config.get('PEAKSEARCH', 'boxsize'))
        
        try:
            fit_peaks_gaussian_global = int(config.get('PEAKSEARCH', 'fit_peaks_gaussian'))
        except:
            self.write_to_console("Fitting of peaks not defined, using default Gaussian fitting")
        self.fit_peaks_gaussian_global = fit_peaks_gaussian_global
        
        try:
            FitPixelDev_global = float(config.get('PEAKSEARCH', 'FitPixelDev'))
        except:
            self.write_to_console("Fitting PixelDev of peaks not defined, using default 20 pix")
        self.FitPixelDev_global=FitPixelDev_global
        
        try:
            NumberMaxofFits = float(config.get('PEAKSEARCH', 'NumberMaxofFits'))
        except:
            self.write_to_console("Max fits per LP not defined, using default 3000")
        self.NumberMaxofFits=NumberMaxofFits
        
        try:
            strain_label_global = config.get('STRAINCALCULATION', 'strain_compute') == "true"
            if strain_label_global:
                strain_label_global = "YES"
            else:
                strain_label_global = "NO"
        except:
            strain_label_global = "NO"
            self.write_to_console("Strain computation not defined, default False")
        
        try:
            tolerance_strain_temp = config.get('STRAINCALCULATION', 'tolerance_strain_refinement').split(",")
            tolerance_strain = [float(i) for i in tolerance_strain_temp]
        except:
            self.write_to_console("Strain tolerance material 0 not defined")
        self.tolerance_strain = tolerance_strain
        
        try:
            tolerance_strain_temp1 = config.get('STRAINCALCULATION', 'tolerance_strain_refinement1').split(",")
            tolerance_strain1 = [float(i) for i in tolerance_strain_temp1]
        except:
            self.write_to_console("Strain tolerance for material 1 not defined")
        self.tolerance_strain1 = tolerance_strain1

        try:
            hkls_list_global = config.get('POSTPROCESS', 'hkls_subsets')
        except:
            self.write_to_console("HKL post processing not defined, currently not used")
        
        expfile_global = config.get('EXPERIMENT', 'experiment_directory')
        exp_prefix_global = config.get('EXPERIMENT', 'experiment_file_prefix')
        
        ##exp directory
        if material_global == material1_global:
            fn = material_global + prefix_global
        else:
            fn = material_global + "_" + material1_global + prefix_global
        
        try:
            model_weight_file = config.get('PREDICTION', 'model_weight_file')
        except:
            model_weight_file = "none"
        
        modelfile_global = main_directory + "//" + fn
        if material_global == material1_global:
            if model_weight_file == "none":
                weightfile_global = modelfile_global + "//" + "model_" + material_global + ".h5"
            else:
                weightfile_global = model_weight_file
        else:
            if model_weight_file == "none":
                weightfile_global = modelfile_global + "//" + "model_" + material_global + "_" + material1_global + ".h5"
            else:
                weightfile_global = model_weight_file
        
        try:
            freq_rmv_global = int(config.get('TRAINING', 'classes_with_frequency_to_remove'))
        except:
            self.write_to_console("Frequency removal for HKLs not defined, can be defined in the config window")
        
        try:
            elements_global = config.get('TRAINING', 'desired_classes_output')
        except:
            self.write_to_console("Elements for HKLs not defined, can be defined in the config window")
        try:
            hkl_max_global = config.get('TRAINING', 'max_HKL_index')
        except:
            self.write_to_console("Max HKLs not defined, can be defined in the config window")
        try:
            nb_grains_per_lp_global = int(config.get('TRAINING', 'max_nb_grains'))
        except:
            self.write_to_console("Nb. of grains per LP not defined, can be defined in the config window")
        try:
            freq_rmv1_global = int(config.get('TRAINING', 'classes_with_frequency_to_remove1'))
        except:
            self.write_to_console("Frequency removal for HKLs 1 not defined, can be defined in the config window")
        try:
            elements1_global = config.get('TRAINING', 'desired_classes_output1')
        except:
            self.write_to_console("Elements for HKLs 1 not defined, can be defined in the config window")
        try:
            hkl_max1_global = config.get('TRAINING', 'max_HKL_index1')
        except:
            self.write_to_console("Max HKLs 1 not defined, can be defined in the config window")
        try:
            nb_grains_per_lp1_global = int(config.get('TRAINING', 'max_nb_grains1'))
        except:
            self.write_to_console("Nb. of grains per LP 1 not defined, can be defined in the config window")
        try:
            maximum_angle_to_search_global = float(config.get('TRAINING', 'angular_distance'))
        except:
            self.write_to_console("Histogram angle not defined, can be defined in the config window")
        try:
            step_for_binning_global = float(config.get('TRAINING', 'step_size'))
        except:
            self.write_to_console("steps for histogram binnning not defined, can be defined in the config window")
        try:
            grains_nb_simulate_global = int(config.get('TRAINING', 'max_simulations'))
        except:
            self.write_to_console("Number of simulations per LP not defined, can be defined in the config window")
        try:
            include_scm_global = config.get('TRAINING', 'include_small_misorientation') == "true"
        except:
            self.write_to_console("Single crystal misorientation not defined, can be defined in the config window")
        try:
            misorientation_angle = float(config.get('TRAINING', 'misorientation_angle'))
        except:
            misorientation_angle = misorientation_angle1
            self.write_to_console("Angle of Single crystal misorientation along Z not defined, can be defined in the config window")
        self.misorientation_angle = misorientation_angle
        try:
            batch_size_global = int(config.get('TRAINING', 'batch_size'))
        except:
            self.write_to_console("Batch size not defined, can be defined in the config window")
        try:
            epochs_global = int(config.get('TRAINING', 'epochs'))
        except:
            self.write_to_console("Epochs not defined, can be defined in the config window")
        
        try:
            cap_matchrate = float(config.get('PREDICTION', 'cap_matchrate')) * 100
        except:
            self.write_to_console("Cap_Matching rate not defined, setting default value of 1%")
        self.cap_matchrate=cap_matchrate
        try:
            tolerance_global = float(config.get('PREDICTION', 'matrix_tolerance'))
        except:
            self.write_to_console("Angle tolerance to detect grains not defined, using default 0.7")
        try:
            tolerance_global1 = float(config.get('PREDICTION', 'matrix_tolerance1'))
        except:
            self.write_to_console("Angle tolerance for Mat 1 to detect grains not defined, using default 0.7")
        try:
            use_previous_UBmatrix = config.get('PREDICTION', 'use_previous') == "true"
        except:
            self.write_to_console("Use previous solutions not defined, using default value False")
        self.use_previous_UBmatrix = use_previous_UBmatrix
        try:
            material_phase_always_present = config.get('DEVELOPMENT', 'material_phase_always_present')
        except:
            material_phase_always_present = "none"
            self.write_to_console("material_phase_always_present not defined, default is NONE")
            
        if material_phase_always_present == "none":
            material_phase_always_present = None
        else:
            material_phase_always_present = int(material_phase_always_present)
        self.material_phase_always_present = material_phase_always_present
        try:
            write_mtex_file = config.get('DEVELOPMENT', 'write_MTEX_file') == "true"
        except:
            self.write_to_console("Write MTEX texture file not defined, by default True")
        try:
            material0_lauegroup = config.get('DEVELOPMENT', 'material0_lauegroup')
        except:
            self.write_to_console("Laue group of first material not defined, can be defined in the config windoby default Cubic")
        try:
            material1_lauegroup = config.get('DEVELOPMENT', 'material1_lauegroup')
        except:
            self.write_to_console("Laue group of second material not defined, can be defined in the config windoby default Cubic")
                  
        self.write_to_console("Config file loaded successfully.")
        # except:
        #     self.write_to_console("Config file Error.")

    def _createToolBar(self):
        self.tools = QToolBar()
        self.addToolBar(self.tools)
        self.trialtoolbar101 = self.tools.addAction('Example_config', self.show_window_config)
        self.trialtoolbar10 = self.tools.addAction('Re-Train saved model', self.show_window_retraining_fromfile)
        self.trialtoolbar1 = self.tools.addAction('Re-Train GUI model', self.show_window_retraining)
        self.trialtoolbar10.setEnabled(False)
        self.trialtoolbar1.setEnabled(False)
        
    def show_window_parameters(self):
        w2 = AnotherWindowParams(self.state, gui_state)
        w2.got_signal.connect(self.postprocesstrain)
        w2.show()
        self.popups.append(w2)
        self.state = self.state +1
    
    def show_window_retraining(self):
        ct = time.time()
        now = datetime.datetime.fromtimestamp(ct)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.train_model(prefix="_"+c_time, tag = 1)
        
    def show_window_retraining_fromfile(self):
        ct = time.time()
        now = datetime.datetime.fromtimestamp(ct)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        self.train_model(prefix="_"+c_time, tag = 2)
        
    def show_window_config(self):
        w21 = sample_config()
        w21.show()
        self.popups.append(w21)
        
    def show_window_liveprediction(self):
        if self.material_ != self.material1_:
            with open(self.save_directory+"//classhkl_data_nonpickled_"+self.material_+".pickle", "rb") as input_file:
                hkl_all_class0 = cPickle.load(input_file)[0]

            with open(self.save_directory+"//classhkl_data_nonpickled_"+self.material1_+".pickle", "rb") as input_file:
                hkl_all_class1 = cPickle.load(input_file)[0]

        else:
            hkl_all_class1 = None
            with open(self.save_directory+"//classhkl_data_nonpickled_"+self.material_+".pickle", "rb") as input_file:
                hkl_all_class0 = cPickle.load(input_file)[0]
        
        w2 = AnotherWindowLivePrediction(self.state2, gui_state, 
                                         material_=self.material_, material1_=self.material1_, emin=self.emin, 
                                         emax=self.emax, symmetry=self.symmetry, symmetry1=self.symmetry1,
                                         detectorparameters=self.detectorparameters, pixelsize=self.pixelsize,
                                         lattice_=self.lattice_material, lattice1_ =self.lattice_material1,
                                         hkl_all_class0 = hkl_all_class0, hkl_all_class1=hkl_all_class1,
                                         mode_spotCycleglobal=self.mode_spotCycleglobal,
                                         softmax_threshold_global = self.softmax_threshold_global,
                                         mr_threshold_global =    self.mr_threshold_global,
                                         cap_matchrate =    self.cap_matchrate,
                                         coeff =    self.coeff,
                                         coeff_overlap1212 =    self.coeff_overlap,
                                         fit_peaks_gaussian_global =    self.fit_peaks_gaussian_global,
                                         FitPixelDev_global =    self.FitPixelDev_global,
                                         NumberMaxofFits =    self.NumberMaxofFits,
                                         tolerance_strain =    self.tolerance_strain,
                                         tolerance_strain1 =    self.tolerance_strain1,
                                         material0_limit = self.material0_limit,
                                         material1_limit = self.material1_limit,
                                         symmetry_name = self.symmetry_name, 
                                         symmetry1_name = self.symmetry1_name,
                                         use_previous_UBmatrix_name = self.use_previous_UBmatrix,
                                         material_phase_always_present = self.material_phase_always_present,
                                         crystal=self.crystal, crystal1=self.crystal1)
        w2.show()
        self.popups.append(w2)
        self.state2 += 1
        
    def _createStatusBar(self):
        self.status = QStatusBar()
        self.status.showMessage("status")
        self.setStatusBar(self.status)

    def _formLayout(self):
        self.formLayout = QFormLayout()
        
        self.progress = QProgressBar()
        
        self.configure_nn = QPushButton('Configure parameters')
        self.configure_nn.clicked.connect(self.show_window_parameters)
        self.configure_nn.setEnabled(True)
        
        self.generate_nn = QPushButton('Generate Training dataset')
        self.generate_nn.clicked.connect(self.generate_training_data)
        self.generate_nn.setEnabled(False)
        
        self.train_nn = QPushButton('Train Neural Network')
        self.train_nn.clicked.connect(self.train_neural_network)
        self.train_nn.setEnabled(False)
        
        self.train_nnhp = QPushButton('Hypergrid Params OPT')
        self.train_nnhp.clicked.connect(self.grid_search_hyperparams)
        self.train_nnhp.setEnabled(False)

        self.predict_lnn = QPushButton('Live Prediction with IPF map')
        self.predict_lnn.clicked.connect(self.show_window_liveprediction)
        self.predict_lnn.setEnabled(False)
        
        self.formLayout.addRow(self.progress)
        self.formLayout.addRow(self.configure_nn)
        self.formLayout.addRow(self.generate_nn)
        self.formLayout.addRow(self.train_nn)
        self.formLayout.addRow(self.train_nnhp)
        self.formLayout.addRow(self.predict_lnn)
        self.layout.addLayout(self.formLayout)
        
    def write_to_console(self, line, to_push=0):
        try:
            self.text_file_log.write(line + "\n")
        except:
            print("Log file not yet created: "+ str(line.encode('utf-8','ignore')))
        self.setDisplayText(str(line.encode('utf-8','ignore'),errors='ignore'))
        QApplication.processEvents() 
    
    def postprocesstrain(self, emit_dict):
        self.input_params = {
                            "material_": emit_dict["material_"], ## same key as used in LaueTools
                            "material1_": emit_dict["material1_"],
                            "prefix": emit_dict["prefix"],
                            "symmetry": emit_dict["symmetry"],
                            "symmetry1": emit_dict["symmetry1"],
                            "hkl_max_identify" : emit_dict["hkl_max_identify"], # can be "auto" or an index i.e 12
                            "hkl_max_identify1" : emit_dict["hkl_max_identify1"],
                            "maximum_angle_to_search" : emit_dict["maximum_angle_to_search"],
                            "step_for_binning" : emit_dict["step_for_binning"],
                            "mode_of_analysis" : emit_dict["mode_of_analysis"],
                            "nb_grains_per_lp" : emit_dict["nb_grains_per_lp"], ## max grains to expect in a LP
                            "nb_grains_per_lp1" : emit_dict["nb_grains_per_lp1"],
                            "grains_nb_simulate" : emit_dict["grains_nb_simulate"],
                            "detectorparameters" : emit_dict["detectorparameters"],
                            "pixelsize" : emit_dict["pixelsize"],
                            "dim1" : emit_dict["dim1"],
                            "dim2" : emit_dict["dim2"],
                            "emin" : emit_dict["emin"],
                            "emax" : emit_dict["emax"],
                            "batch_size" : emit_dict["batch_size"], ## batches of files to use while training
                            "epochs" : emit_dict["epochs"], ## number of epochs for training
                            "texture": emit_dict["texture"],
                            "mode_nn": emit_dict["mode_nn"],
                            "grid_bool": emit_dict["grid_bool"],
                            "directory": emit_dict["directory"],
                            "freq_rmv":  emit_dict["freq_rmv"],
                            "elements":  emit_dict["elements"],
                            "freq_rmv1":  emit_dict["freq_rmv1"],
                            "elements1":  emit_dict["elements1"],
                            "include_scm":  emit_dict["include_scm"],
                            "lr":  emit_dict["lr"],
                            "kc":  emit_dict["kc"],
                            "bc":  emit_dict["bc"],
                            }
        ## Gray out options based on the mode_nn
        if self.input_params["mode_nn"] == "Generate Data & Train":
            self.write_to_console("Generate and Train the Model")
            self.generate_nn.setEnabled(True)
            
        elif self.input_params["mode_nn"] == "Train":
            self.write_to_console("Data already exists ? Train the Model")
            self.train_nn.setEnabled(True)
            self.trialtoolbar10.setEnabled(True)
            
        elif self.input_params["mode_nn"] == "Predict":
            self.write_to_console("Model already exists? Lets Predict!")
            self.write_to_console("on the fly prediction (fingers crossed)")
            # self.predict_nn.setEnabled(True)
            # self.predict_nnc.setEnabled(True)
            self.predict_lnn.setEnabled(True)

        if self.input_params["grid_bool"] == "True":
            self.train_nnhp.setEnabled(True)
        
        self.include_scm = False
        if self.input_params["include_scm"] == "yes":
            self.include_scm = True  
            
        self.freq_rmv = self.input_params["freq_rmv"]
        self.freq_rmv1 = self.input_params["freq_rmv1"]
        if self.input_params["elements"] == "all":
            self.elements = self.input_params["elements"] #"all"
            self.elements1 = self.input_params["elements1"] #"all"
        else:
            self.elements = int(self.input_params["elements"])
            self.elements1 = int(self.input_params["elements1"])
            
        self.material_ = self.input_params["material_"]
        self.material1_ = self.input_params["material1_"]
        
        self.emin, self.emax = self.input_params["emin"], self.input_params["emax"]
        
        self.learning_rate, self.kernel_coeff, self.bias_coeff = self.input_params["lr"],self.input_params["kc"],self.input_params["bc"]
        
        if self.input_params["directory"] == None: ## default path
            if self.material_ == self.material1_:
                self.save_directory = os.getcwd()+"//"+self.input_params["material_"]+self.input_params["prefix"]
            else:
                self.save_directory = os.getcwd()+"//"+self.input_params["material_"]+"_"+self.input_params["material1_"]+self.input_params["prefix"]
        else:
            if self.material_ == self.material1_:
                self.save_directory = self.input_params["directory"]+"//"+self.input_params["material_"]+self.input_params["prefix"]
            else:
                self.save_directory = self.input_params["directory"]+"//"+self.input_params["material_"]+"_"+self.input_params["material1_"]+self.input_params["prefix"]

        self.n = self.input_params["hkl_max_identify"]
        self.n1 = self.input_params["hkl_max_identify1"]
        self.maximum_angle_to_search = self.input_params["maximum_angle_to_search"]
        self.step_for_binning = self.input_params["step_for_binning"]
        self.mode_of_analysis = self.input_params["mode_of_analysis"]
        self.nb_grains_per_lp = self.input_params["nb_grains_per_lp"]
        self.nb_grains_per_lp1 = self.input_params["nb_grains_per_lp1"]
        self.grains_nb_simulate = self.input_params["grains_nb_simulate"]
        self.detectorparameters = self.input_params["detectorparameters"]
        self.pixelsize = self.input_params["pixelsize"]
        # =============================================================================
        # Symmetry input
        # =============================================================================
        a, b, c, alpha, beta, gamma = dictLT.dict_Materials[self.material_][1]
        # a, b, c = a*0.1, b*0.1, c*0.1
        if self.SG == None:
            if self.input_params["symmetry"] =="cubic":
                self.SG = 230
            elif self.input_params["symmetry"] =="monoclinic":
                self.SG = 10
            elif self.input_params["symmetry"] == "hexagonal":
                self.SG = 191
            elif self.input_params["symmetry"] == "orthorhombic":
                self.SG = 47
            elif self.input_params["symmetry"] == "tetragonal":
                self.SG = 123
            elif self.input_params["symmetry"] == "trigonal":
                self.SG = 162
            elif self.input_params["symmetry"] == "triclinic":
                self.SG = 2
        
        self.rules = dictLT.dict_Materials[self.material_][-1]
        self.symmetry_name = self.input_params["symmetry"]
        if self.input_params["symmetry"] =="cubic":
            self.crystal = SGLattice(int(self.SG), a)
            self.symmetry = Symmetry.cubic
            self.lattice_material = Lattice.cubic(a)
        elif self.input_params["symmetry"] =="monoclinic":
            self.crystal = SGLattice(int(self.SG),a, b, c, beta)
            self.symmetry = Symmetry.monoclinic
            self.lattice_material = Lattice.monoclinic(a, b, c, beta)
        elif self.input_params["symmetry"] == "hexagonal":
            self.crystal = SGLattice(int(self.SG),a, c)
            self.symmetry = Symmetry.hexagonal
            self.lattice_material = Lattice.hexagonal(a, c)
        elif self.input_params["symmetry"] == "orthorhombic":
            self.crystal = SGLattice(int(self.SG),a, b, c)
            self.symmetry = Symmetry.orthorhombic
            self.lattice_material = Lattice.orthorhombic(a, b, c)
        elif self.input_params["symmetry"] == "tetragonal":
            self.crystal = SGLattice(int(self.SG),a, c)
            self.symmetry = Symmetry.tetragonal
            self.lattice_material = Lattice.tetragonal(a, c)
        elif self.input_params["symmetry"] == "trigonal":
            self.crystal = SGLattice(int(self.SG),a, alpha)
            self.symmetry = Symmetry.trigonal
            self.lattice_material = Lattice.rhombohedral(a, alpha)
        elif self.input_params["symmetry"] == "triclinic":
            self.crystal = SGLattice(int(self.SG),a, b, c, alpha, beta, gamma)
            self.symmetry = Symmetry.triclinic
            self.lattice_material = Lattice.triclinic(a, b, c, alpha, beta, gamma)
        # self.symmetry.operation_rotation = self.crystal._hklsym
        # self.lattice_material.sglattice = self.crystal
        
        if self.material_ != self.material1_:
            
            if self.SG1 == None:
                if self.input_params["symmetry1"] =="cubic":
                    self.SG1 = 230
                elif self.input_params["symmetry1"] =="monoclinic":
                    self.SG1 = 10
                elif self.input_params["symmetry1"] == "hexagonal":
                    self.SG1 = 191
                elif self.input_params["symmetry1"] == "orthorhombic":
                    self.SG1 = 47
                elif self.input_params["symmetry1"] == "tetragonal":
                    self.SG1 = 123
                elif self.input_params["symmetry1"] == "trigonal":
                    self.SG1 = 162
                elif self.input_params["symmetry1"] == "triclinic":
                    self.SG1 = 2
            
            self.symmetry1_name = self.input_params["symmetry1"]
            a1, b1, c1, alpha1, beta1, gamma1 = dictLT.dict_Materials[self.material1_][1]
            self.rules1 = dictLT.dict_Materials[self.material1_][-1]
            if self.input_params["symmetry1"] =="cubic":
                self.crystal1 = SGLattice(int(self.SG1), a1)
                self.symmetry1 = Symmetry.cubic
                self.lattice_material1 = Lattice.cubic(a1)
            elif self.input_params["symmetry1"] =="monoclinic":
                self.crystal1 = SGLattice(int(self.SG1),a1, b1, c1, beta1)
                self.symmetry1 = Symmetry.monoclinic
                self.lattice_material1 = Lattice.monoclinic(a1, b1, c1, beta1)
            elif self.input_params["symmetry1"] == "hexagonal":
                self.crystal1 = SGLattice(int(self.SG1),a1, c1)
                self.symmetry1 = Symmetry.hexagonal
                self.lattice_material1 = Lattice.hexagonal(a1, c1)
            elif self.input_params["symmetry1"] == "orthorhombic":
                self.crystal1 = SGLattice(int(self.SG1),a1, b1, c1)
                self.symmetry1 = Symmetry.orthorhombic
                self.lattice_material1 = Lattice.orthorhombic(a1, b1, c1)
            elif self.input_params["symmetry1"] == "tetragonal":
                self.crystal1 = SGLattice(int(self.SG1),a1, c1)
                self.symmetry1 = Symmetry.tetragonal
                self.lattice_material1 = Lattice.tetragonal(a1, c1)
            elif self.input_params["symmetry1"] == "trigonal":
                self.crystal1 = SGLattice(int(self.SG1),a1, alpha1)
                self.symmetry1 = Symmetry.trigonal
                self.lattice_material1 = Lattice.rhombohedral(a1, alpha1)
            elif self.input_params["symmetry1"] == "triclinic":
                self.crystal1 = SGLattice(int(self.SG1),a1, b1, c1, alpha1, beta1, gamma1)
                self.symmetry1 = Symmetry.triclinic
                self.lattice_material1 = Lattice.triclinic(a1, b1, c1, alpha1, beta1, gamma1)
            # self.symmetry1.operation_rotation = self.crystal1._hklsym
            # self.lattice_material1.sglattice = self.crystal1
        else:
            self.rules1 = None
            self.symmetry1 = None
            self.lattice_material1 = None
            self.crystal1 = None
            self.symmetry1_name = self.input_params["symmetry"]
        
        self.modelp = "random" 
        ### Load texture files based on symmetry
        if self.input_params["texture"] == "in-built_Uniform_Distribution":
            self.write_to_console("# Using uniform distribution generated with Neper for Training dataset \n") 
            self.modelp = "uniform"
        elif self.input_params["texture"] == "random":
            self.write_to_console("# Using random orientation distribution for Training dataset \n") 
            self.modelp = "random"
        else:
            self.modelp = "experimental"
            self.write_to_console("# User defined texture to be used: TODO \n") 
        
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        self.write_to_console("Working directory :"+ self.save_directory)
        
        ## Golbal log file
        now = datetime.datetime.fromtimestamp(GUI_START_TIME)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        if self.material_ == self.material1_:
            self.text_file_log = open(self.save_directory+"//log_"+self.material_+".txt", "a")
        else:
            self.text_file_log = open(self.save_directory+"//log_"+self.material_+"_"+self.material1_+".txt", "a")
        self.text_file_log.write("# Log file created at "+ c_time + "\n") 

    def temp_HKL(self, removeharmonics=1):
        material_= self.input_params["material_"]
        nbgrains = self.input_params["nb_grains_per_lp"]
        nbtestspots = 0
        hkl_sol_all = np.zeros((1,4))
        verbose=0
        for _ in range(10):
            seednumber = np.random.randint(1e6)
            tabledistancerandom, hkl_sol, \
                                    _, _, _, _, _ = self.prepare_LP(nbgrains, 0,
                                                                    material_,
                                                                    None,
                                                                    verbose,
                                                                    plotLauePattern=False,
                                                                    seed=seednumber,
                                                                    detectorparameters=self.input_params["detectorparameters"], 
                                                                    pixelsize=self.input_params["pixelsize"],
                                                                    dim1=self.input_params["dim1"],
                                                                    dim2=self.input_params["dim2"],
                                                                    removeharmonics=removeharmonics)
                                    
            spots_in_center = [sp for sp in range(len(tabledistancerandom))] # take all spots in Laue pattern
            hkl_sol_all = np.vstack((hkl_sol_all, hkl_sol))
            nbtestspots = nbtestspots + len(spots_in_center)

        if self.material_ != self.material1_:
            copy1 = np.copy(int(np.max(np.abs(hkl_sol_all))))
            copy1_min = np.copy(int(np.min(hkl_sol_all)))
            material_= self.input_params["material1_"]
            nbgrains = self.input_params["nb_grains_per_lp1"]
            hkl_sol_all = np.zeros((1,4))
            verbose=0
            for _ in range(10):
                seednumber = np.random.randint(1e6)
                tabledistancerandom, hkl_sol, \
                                        _, _, _, _, _ = self.prepare_LP(nbgrains, 0,
                                                                        material_,
                                                                        None,
                                                                        verbose,
                                                                        plotLauePattern=False,
                                                                        seed=seednumber,
                                                                        detectorparameters=self.input_params["detectorparameters"], 
                                                                        pixelsize=self.input_params["pixelsize"],
                                                                        dim1=self.input_params["dim1"],
                                                                        dim2=self.input_params["dim2"],
                                                                        removeharmonics=removeharmonics)
                                        
                spots_in_center = [sp for sp in range(len(tabledistancerandom))] # take all spots in Laue pattern
                hkl_sol_all = np.vstack((hkl_sol_all, hkl_sol))
                nbtestspots = nbtestspots + len(spots_in_center)
            hkl_sol_all = np.delete(hkl_sol_all, 0, axis =0)
            copy_ = np.copy(int(np.max(np.abs(hkl_sol_all))))
            copy_min_ = np.copy(int(np.min(hkl_sol_all)))
            self.write_to_console("Total spots created for calculating HKL bounds:"+str(nbtestspots))
            self.write_to_console("Max HKL index for "+self.material_+" :"+str(copy1))
            self.write_to_console("Min HKL index "+self.material_+" :"+str(copy1_min))
            self.write_to_console("Max HKL index for "+self.material1_+" :"+str(copy_))
            self.write_to_console("Min HKL index "+self.material1_+" :"+str(copy_min_))
            return int(copy1), int(copy_)

        self.write_to_console("Total spots created for calculating HKL bounds:"+str(nbtestspots))
        self.write_to_console("Max HKL index:"+str(np.max(hkl_sol_all)))
        self.write_to_console("Min HKL index:"+str(np.min(hkl_sol_all)))
        return int(np.max(np.abs(hkl_sol_all))), int(np.max(np.abs(hkl_sol_all)))
    
    def prepare_LP(self, nbgrains, nbgrains1, material_, material1_, verbose, plotLauePattern, seed=None, sortintensity=False,
                   detectorparameters=None, pixelsize=None, dim1=2048, dim2=2048, removeharmonics=1):
        s_tth, s_chi, s_miller_ind, s_posx, s_posy, \
                                        s_intensity, _, _ = simulatemultiplepatterns(nbgrains, nbgrains1, seed=seed, 
                                                                                    key_material=material_,
                                                                                    key_material1=material1_,
                                                                                    detectorparameters=detectorparameters,
                                                                                    pixelsize=pixelsize,
                                                                                    emin=self.emin,
                                                                                    emax=self.emax,
                                                                                    sortintensity=sortintensity, 
                                                                                    dim1=dim1,dim2=dim2,
                                                                                    removeharmonics=removeharmonics,
                                                                                    misorientation_angle=1)
        # considering all spots
        allspots_the_chi = np.transpose(np.array([s_tth/2., s_chi]))
        tabledistancerandom = np.transpose(GT.calculdist_from_thetachi(allspots_the_chi, allspots_the_chi))
        # ground truth
        hkl_sol = s_miller_ind
        return tabledistancerandom, hkl_sol, s_posx, s_posy, s_intensity, s_tth, s_chi
    
    #TODO
    # Include libraries from the ORIX to take into account spacegroup and symmetry direct
    # later can be used for IPF plots too
    def run_(self, n, rules, lattice_material, symmetry, material_, crystal=None, SG=None, general_diff_cond=False):  
        temp_ = GT.threeindices_up_to(int(n))
        classhkl_ = temp_

        self.write_to_console("Generating HKL objects", to_push=1)
        # generate HKL object
        self.progress.setMaximum(len(classhkl_))
        hkl_all = {}
        # another_method = False
        for i in range(len(classhkl_)):
            new_hkl = classhkl_[i,:]
            
            if general_diff_cond:
                cond_proceed = crystal.hkl_allowed(new_hkl, returnequivalents=False)
            else:
                cond_proceed = True
            
            if not cond_proceed:
                continue
            
            new_rounded_hkl = _round_indices(new_hkl)
            mul_family = crystal.equivalent_hkls(new_rounded_hkl)
            
            family = []
            for sym in mul_family:
                family.append(sym)
            hkl_all[str(new_rounded_hkl)] = {"hkl":new_rounded_hkl, 
                                     "family": family}
            self.progress.setValue(i+1)
            QApplication.processEvents() 

        ## FAST IMPLEMENTATION
        ## make comprehensive list of dictionary
        equ_hkl = np.zeros((1,3))
        for j in hkl_all.keys():
            equ_hkl = np.vstack((equ_hkl, hkl_all[j]["family"]))
        equ_hkl = np.delete(equ_hkl, 0, axis =0)

        index_hkl = [j for j,k in enumerate(hkl_all.keys()) for i in range(len(hkl_all[k]["family"]))]

        self.write_to_console("Removing harmonics and building equivalent HKL objects", to_push=1)
        self.progress.setMaximum(len(hkl_all.keys()))
        ind_rmv = []
        for j1, i1 in enumerate(hkl_all.keys()):
            hkl_1 = hkl_all[i1]["hkl"]
            temp1_ = np.all(hkl_1 == equ_hkl, axis=1)
            if len(np.where(temp1_)[0]) != 0:
                ind_ = np.where(temp1_)[0]
                for inin in ind_:
                    if index_hkl[inin] > j1:
                        ind_rmv.append(i1)
                        break
            self.progress.setValue(j1+1)
            QApplication.processEvents()

        if len(ind_rmv) != 0:
            for inrmv in ind_rmv:
                _ = hkl_all.pop(inrmv, None)
        
        self.write_to_console("Finalizing the HKL objects", to_push=1)
        hkl_all_class = hkl_all
        hkl_millerindices = {}
        classhkl = np.zeros((len(hkl_all),3))
        for j1, i1 in enumerate(hkl_all.keys()):
            hkl_object = hkl_all[i1]["hkl"]
            classhkl[j1,:] = hkl_object
            family = hkl_all_class[i1]["family"]
            hkl_millerindices[i1] =  np.array([ii for ii in family])

        tempdict = hkl_millerindices

        with open(self.save_directory + "//classhkl_data_"+material_+".pickle", "wb") as output_file:
            cPickle.dump([classhkl, classhkl_, ind_rmv, n, temp_, \
                          hkl_all_class, hkl_all, lattice_material, symmetry], output_file)
        
        with open(self.save_directory + "//classhkl_data_nonpickled_"+material_+".pickle", "wb") as output_file:
            cPickle.dump([tempdict], output_file)       
        
        self.write_to_console("Saved class HKL data in : "+self.save_directory + "//classhkl_data_"+material_+".pickle")
    
    def load_dataset(self, material_="Cu", material1_="Cu", ang_maxx=18.,step=0.1, mode=0, 
                     nb_grains=1, nb_grains1=1, grains_nb_simulate=100, data_realism = False, 
                     detectorparameters=None, pixelsize=None, type_="training",
                     var0 = 0, dim1=2048, dim2=2048, removeharmonics=1): 
        """
        works for all symmetries now.
        """
        ## make sure directory exists
        save_directory_ = self.save_directory+"//"+type_
        if not os.path.exists(save_directory_):
            os.makedirs(save_directory_)

        try:
            with open(self.save_directory+"//classhkl_data_"+material_+".pickle", "rb") as input_file:
                classhkl, _, _, n, _, \
                    hkl_all_class, _, lattice_material, symmetry = cPickle.load(input_file)
                    
            if material_ != material1_:
                with open(self.save_directory+"//classhkl_data_"+material1_+".pickle", "rb") as input_file:
                    classhkl1, _, _, n, _, \
                        hkl_all_class1, _, lattice_material1, symmetry1 = cPickle.load(input_file)
        except:
            self.write_to_console("Class HKL library data not found, please run it first")
            return None
        
        max_millerindex = int(n)
        
        if var0==1:
            codebars, angbins = get_material_data(material_ = material_, ang_maxx = ang_maxx, step = step,
                                                       hkl_ref=n, classhkl=classhkl)
            loc = np.array([ij for ij in range(len(classhkl))])

            self.write_to_console("Verifying if two different HKL class have same angular distribution (can be very time consuming depending on the symmetry)")
            index = []
            self.progress.setMaximum(len(codebars))
            list_appended = []
            count_cbs = 0
            for i, j in enumerate(codebars):
                for k, l in enumerate(codebars):
                    if i in list_appended and k in list_appended:
                        continue
                    if i != k and np.all(j == l):
                        index.append((i,k))
                        string0 = "HKL's "+ str(classhkl[i])+" and "+str(classhkl[k])+" have exactly the same angular distribution."
                        self.write_to_console(string0)
                    list_appended.append(i)
                    list_appended.append(k)
                count_cbs += 1
                self.progress.setValue(count_cbs)
                QApplication.processEvents()
                  
            if len(index) == 0:
                self.write_to_console("Great! No two HKL class have same angular distribution")
                #np.savez_compressed(save_directory_+'//grain_init.npz', codebars, loc)
            else:
                self.write_to_console("Some HKL's have similar angular distribution; this will likely reduce the accuracy of the neural network; verify if symmetry matrix and other parameters are properly configured; this is just for the dictionary; keep eye on the dataset being generated for training")
                self.write_to_console("This is likely the result of the symmetry operation available in a user_defined space group; this shouldn't affect the general accuracy of the model")
                np.savez_compressed(self.save_directory+'//conflict_angular_distribution_debug.npz', codebars, index)           
            np.savez_compressed(self.save_directory+'//grain_classhkl_angbin.npz', classhkl, angbins)
                 
            if material_ != material1_:
                codebars, angbins = get_material_data(material_ = material1_, ang_maxx = ang_maxx, step = step,
                                                       hkl_ref=n, classhkl=classhkl1)
                ind_offset = loc[-1] + 1
                loc = np.array([ind_offset + ij for ij in range(len(classhkl1))])
                self.write_to_console("Verifying if two different HKL class have same angular distribution (can be very time consuming depending on the symmetry)")
                index = []
                self.progress.setMaximum(len(codebars))
                list_appended = []
                count_cbs = 0
                for i, j in enumerate(codebars):
                    for k, l in enumerate(codebars):
                        if i in list_appended and k in list_appended:
                            continue
                        if i != k and np.all(j == l):
                            index.append((i,k))
                            string0 = "HKL's "+ str(classhkl1[i])+" and "+str(classhkl1[k])+" have exactly the same angular distribution."
                            self.write_to_console(string0)
                        list_appended.append(i)
                        list_appended.append(k)
                    count_cbs += 1
                    self.progress.setValue(count_cbs)
                    QApplication.processEvents()

                if len(index) == 0:
                    self.write_to_console("Great! No two HKL class have same angular distribution")
                    #np.savez_compressed(save_directory_+'//grain_init1.npz', codebars, loc)
                else:
                    self.write_to_console("Some HKL's have similar angular distribution; this will likely reduce the accuracy of the neural network; verify if symmetry matrix and other parameters are properly configured; this is just for the dictionary; keep eye on the dataset being generated for training")
                    self.write_to_console("This is likely the result of the symmetry operation available in a user_defined space group; this shouldn't affect the general accuracy of the model")
                    np.savez_compressed(self.save_directory+'//conflict_angular_distribution1_debug.npz', codebars, index)                
                np.savez_compressed(self.save_directory+'//grain_classhkl_angbin1.npz', classhkl1, angbins)
        
        ## make comprehensive list of dictionary    
        normal_hkl_ = np.zeros((1,3))
        for j in hkl_all_class.keys():
            normal_hkl_ = np.vstack((normal_hkl_, hkl_all_class[j]["family"]))
        normal_hkl = np.delete(normal_hkl_, 0, axis =0)
        
        if material_ != material1_:
            normal_hkl1_ = np.zeros((1,3))
            for j in hkl_all_class1.keys():
                normal_hkl1_ = np.vstack((normal_hkl1_, hkl_all_class1[j]["family"]))
            normal_hkl1 = np.delete(normal_hkl1_, 0, axis =0)
        
        index_hkl = [j for j,k in enumerate(hkl_all_class.keys()) for i in range(len(hkl_all_class[k]["family"]))]
        
        if material_ != material1_:
            ind_offset = index_hkl[-1] + 1
            index_hkl1 = [ind_offset+j for j,k in enumerate(hkl_all_class1.keys()) for i in range(len(hkl_all_class1[k]["family"]))]

        if material_ == material1_:
            index_hkl1 = None
            normal_hkl1 = None
            classhkl1 = None
            hkl_all_class1 = None
            lattice_material1 = None
            symmetry1 = None
        
        self.write_to_console("Generating "+type_+" and saving them")
        
        if material_ != material1_:
            nb_grains_list = list(range(nb_grains+1))
            nb_grains1_list = list(range(nb_grains1+1))
            list_permute = list(itertools.product(nb_grains_list, nb_grains1_list))
            list_permute.pop(0)
            max_progress = len(list_permute)*grains_nb_simulate
        else:
            max_progress = nb_grains*grains_nb_simulate
        if self.include_scm:
            max_progress = max_progress + grains_nb_simulate
            if material_ != material1_:
                 max_progress = max_progress + 2*grains_nb_simulate
                     
        self.progress.setMaximum(max_progress)

        self._inputs_queue = Queue()
        self._outputs_queue = Queue()
        self._worker_process = {}
        for i in range(self.ncpu):
            self._worker_process[i]= Process(target=worker_generation, args=(self._inputs_queue, 
                                                                              self._outputs_queue, 
                                                                              i+1),)
        for i in range(self.ncpu):
            self._worker_process[i].start()            
        time.sleep(0.1)    
        
        if material_ != material1_:
            if self.modelp == "uniform":
                
                if grains_nb_simulate <= 2000:
                    if type_ =="training_data":
                        xlim, ylim = 0, int(0.8*2000)
                    else:
                        xlim, ylim = int(0.8*2000), 2000-1
                    path_array = resource_path("uniform_orientations_2000.npz")
                else: ## 10000 orientation list
                    if type_ =="training_data":
                        xlim, ylim = 0, int(0.8*10000)
                    else:
                        xlim, ylim = int(0.8*10000), 10000-1
                    path_array = resource_path("uniform_orientations.npz")
                arr = np.load(path_array)
                
                if symmetry == symmetry.cubic:
                    odf_data = arr["arr_6"][xlim:ylim]
                    print("Laue group 11")
                elif symmetry == symmetry.hexagonal:
                    odf_data = arr["arr_5"][xlim:ylim]
                    print("Laue group 9")
                elif symmetry == symmetry.trigonal:
                    odf_data = arr["arr_4"][xlim:ylim]
                    print("Laue group 7")
                elif symmetry == symmetry.tetragonal:
                    odf_data = arr["arr_3"][xlim:ylim]
                    print("Laue group 5")
                elif symmetry == symmetry.orthorhombic:
                    odf_data = arr["arr_2"][xlim:ylim]
                    print("Laue group 3")
                elif symmetry == symmetry.monoclinic:
                    odf_data = arr["arr_1"][xlim:ylim]
                    print("Laue group 2")
                elif symmetry == symmetry.triclinic:
                    odf_data = arr["arr_0"][xlim:ylim]
                    print("Laue group 1")
                                    
                if symmetry1 == symmetry.cubic:
                    odf_data1 = arr["arr_6"][xlim:ylim]
                    print("Laue group 11")
                elif symmetry1 == symmetry.hexagonal:
                    odf_data1 = arr["arr_5"][xlim:ylim]
                    print("Laue group 9")
                elif symmetry1 == symmetry.trigonal:
                    odf_data1 = arr["arr_4"][xlim:ylim]
                    print("Laue group 7")
                elif symmetry1 == symmetry.tetragonal:
                    odf_data1 = arr["arr_3"][xlim:ylim]
                    print("Laue group 5")
                elif symmetry1 == symmetry.orthorhombic:
                    odf_data1 = arr["arr_2"][xlim:ylim]
                    print("Laue group 3")
                elif symmetry1 == symmetry.monoclinic:
                    odf_data1 = arr["arr_1"][xlim:ylim]
                    print("Laue group 2")
                elif symmetry1 == symmetry.triclinic:
                    odf_data1 = arr["arr_0"][xlim:ylim]
                    print("Laue group 1")
            ## list of combination of training dataset
            ## to be seen if this improves the prediction quality
            ## increases time significantly to generate the data 
            nb_grains_list = list(range(nb_grains+1))
            nb_grains1_list = list(range(nb_grains1+1))
            list_permute = list(itertools.product(nb_grains_list, nb_grains1_list))
            list_permute.pop(0) ## removing the 0,0 index
 
            # Idea 2 Or generate a database upto n grain LP
            values = []
            for i in range(len(list_permute)):
                ii, jj = list_permute[i]
                
                for j in range(grains_nb_simulate):
                    if data_realism:
                        ## three types of data augmentation to mimic reality ?
                        if j < grains_nb_simulate*0.25:
                            noisy_data = False
                            remove_peaks = False
                        elif (j >= grains_nb_simulate*0.25) and (j < grains_nb_simulate*0.5):
                            noisy_data = True
                            remove_peaks = False
                        elif (j >= grains_nb_simulate*0.5) and (j < grains_nb_simulate*0.75):
                            noisy_data = False
                            remove_peaks = True
                        elif (j >= grains_nb_simulate*0.75):
                            noisy_data = True
                            remove_peaks = True
                    else:
                        noisy_data = False
                        remove_peaks = False
                    
                    if self.modelp == "uniform":
                        rand_choice = np.random.choice(len(odf_data), ii, replace=False)
                        rand_choice1 = np.random.choice(len(odf_data1), jj, replace=False)
                        data_odf_data = odf_data[rand_choice,:,:]
                        data_odf_data1 = odf_data1[rand_choice1,:,:]
                    else:
                        data_odf_data = None
                        data_odf_data1 = None
                    
                    seednumber = np.random.randint(1e6)
                    values.append([ii, jj, material_,material1_,
                                    self.emin, self.emax, detectorparameters,
                                    pixelsize,True,
                                    ang_maxx, step,
                                    classhkl, classhkl1,
                                    noisy_data, 
                                    remove_peaks,
                                    seednumber,
                                    hkl_all_class,
                                    lattice_material,
                                    None,
                                    normal_hkl,
                                    index_hkl, 
                                    hkl_all_class1,
                                    lattice_material1,
                                    None,
                                    normal_hkl1,
                                    index_hkl1, 
                                    dim1, dim2,
                                    removeharmonics,
                                    0, i, j, save_directory_, 
                                    data_odf_data,
                                    data_odf_data1,
                                    self.modelp,
                                    self.misorientation_angle,
                                    max_millerindex,
                                    self.general_diff_rules,
                                    self.crystal, 
                                    self.crystal1])
                    
            chunks = chunker_list(values, self.ncpu)
            chunks_mp = list(chunks)

            if self.include_scm:
                meta = {'t1':time.time(),
                        'flag':0}
            else:
                meta = {'t1':time.time(),
                        'flag':1}
            for ijk in range(int(self.ncpu)):
                self._inputs_queue.put((chunks_mp[ijk], self.ncpu, meta))

        else:
            # Idea 2 Or generate a database upto n grain LP
            if self.modelp == "uniform":
                ## training split                
                if grains_nb_simulate <= 2000:
                    if type_ =="training_data":
                        xlim, ylim = 0, int(0.8*2000)
                    else:
                        xlim, ylim = int(0.8*2000), 2000-1
                    path_array = resource_path("uniform_orientations_2000.npz")
                else:
                    if type_ =="training_data":
                        xlim, ylim = 0, int(0.8*10000)
                    else:
                        xlim, ylim = int(0.8*10000), 10000-1
                    path_array = resource_path("uniform_orientations.npz")
                arr = np.load(path_array)
                
                if symmetry == symmetry.cubic:
                    odf_data = arr["arr_6"][xlim:ylim]
                    print("Laue group 11")
                elif symmetry == symmetry.hexagonal:
                    odf_data = arr["arr_5"][xlim:ylim]
                    print("Laue group 9")
                elif symmetry == symmetry.trigonal:
                    odf_data = arr["arr_4"][xlim:ylim]
                    print("Laue group 7")
                elif symmetry == symmetry.tetragonal:
                    odf_data = arr["arr_3"][xlim:ylim]
                    print("Laue group 5")
                elif symmetry == symmetry.orthorhombic:
                    odf_data = arr["arr_2"][xlim:ylim]
                    print("Laue group 3")
                elif symmetry == symmetry.monoclinic:
                    odf_data = arr["arr_1"][xlim:ylim]
                    print("Laue group 2")
                elif symmetry == symmetry.triclinic:
                    odf_data = arr["arr_0"][xlim:ylim]
                    print("Laue group 1")

            values = []
            for i in range(nb_grains):
                for j in range(grains_nb_simulate):
                    if data_realism:
                        ## three types of data augmentation to mimic reality ?
                        if j < grains_nb_simulate*0.25:
                            noisy_data = False
                            remove_peaks = False
                        elif (j >= grains_nb_simulate*0.25) and (j < grains_nb_simulate*0.5):
                            noisy_data = True
                            remove_peaks = False
                        elif (j >= grains_nb_simulate*0.5) and (j < grains_nb_simulate*0.75):
                            noisy_data = False
                            remove_peaks = True
                        elif (j >= grains_nb_simulate*0.75):
                            noisy_data = True
                            remove_peaks = True
                    else:
                        noisy_data = False
                        remove_peaks = False
                    
                    if self.modelp == "uniform":
                        rand_choice = np.random.choice(len(odf_data), i+1, replace=False)
                        data_odf_data = odf_data[rand_choice,:,:]
                        data_odf_data1 = None
                    else:
                        data_odf_data = None
                        data_odf_data1 = None
                        
                    seednumber = np.random.randint(1e6)
                    values.append([i+1, 0, material_,material1_,
                                    self.emin, self.emax, detectorparameters,
                                    pixelsize,True,
                                    ang_maxx, step,
                                    classhkl, classhkl1,
                                    noisy_data, 
                                    remove_peaks,
                                    seednumber,
                                    hkl_all_class,
                                    lattice_material,
                                    None,
                                    normal_hkl,
                                    index_hkl, 
                                    hkl_all_class1,
                                    lattice_material1,
                                    None,
                                    normal_hkl1,
                                    index_hkl1, 
                                    dim1, dim2,
                                    removeharmonics,
                                    0, i, j, save_directory_, 
                                    data_odf_data,
                                    data_odf_data1,
                                    self.modelp,
                                    self.misorientation_angle,
                                    max_millerindex,
                                    self.general_diff_rules,
                                    self.crystal, 
                                    self.crystal1])
            chunks = chunker_list(values, self.ncpu)
            chunks_mp = list(chunks)
            
            if self.include_scm:
                meta = {'t1':time.time(),
                        'flag':0}
            else:
                meta = {'t1':time.time(),
                        'flag':1}
            for ijk in range(int(self.ncpu)):
                self._inputs_queue.put((chunks_mp[ijk], self.ncpu, meta))

        if self.include_scm:
            self.write_to_console("Generating small angle misorientation single crystals")  
            values = []
            for i in range(grains_nb_simulate):
                if data_realism:
                    ## three types of data augmentation to mimic reality ?
                    if i < grains_nb_simulate*0.25:
                        noisy_data = False
                        remove_peaks = False
                    elif (i >= grains_nb_simulate*0.25) and (i < grains_nb_simulate*0.5):
                        noisy_data = True
                        remove_peaks = False
                    elif (i >= grains_nb_simulate*0.5) and (i < grains_nb_simulate*0.75):
                        noisy_data = False
                        remove_peaks = True
                    elif (i >= grains_nb_simulate*0.75):
                        noisy_data = True
                        remove_peaks = True
                else:
                    noisy_data = False
                    remove_peaks = False
                seednumber = np.random.randint(1e6)
                values.append([1, 0, material_,material1_,
                                        self.emin, self.emax, detectorparameters,
                                        pixelsize,True,
                                        ang_maxx, step,
                                        classhkl, classhkl1,
                                        noisy_data, 
                                        remove_peaks,
                                        seednumber,
                                        hkl_all_class,
                                        lattice_material,
                                        None,
                                        normal_hkl,
                                        index_hkl, 
                                        hkl_all_class1,
                                        lattice_material1,
                                        None,
                                        normal_hkl1,
                                        index_hkl1, 
                                        dim1, dim2,
                                        removeharmonics,
                                        1, i, i, save_directory_,
                                        None, None, self.modelp,
                                        self.misorientation_angle,
                                        max_millerindex,
                                        self.general_diff_rules,
                                        self.crystal, 
                                        self.crystal1])
                
                if material_ != material1_:
                    seednumber = np.random.randint(1e6)
                    values.append([0, 1, material_,material1_,
                                        self.emin, self.emax, detectorparameters,
                                        pixelsize,True,
                                        ang_maxx, step,
                                        classhkl, classhkl1,
                                        noisy_data, 
                                        remove_peaks,
                                        seednumber,
                                        hkl_all_class,
                                        lattice_material,
                                        None,
                                        normal_hkl,
                                        index_hkl, 
                                        hkl_all_class1,
                                        lattice_material1,
                                        None,
                                        normal_hkl1,
                                        index_hkl1, 
                                        dim1, dim2,
                                        removeharmonics,
                                        2, i, i, save_directory_,
                                        None, None, self.modelp,
                                        self.misorientation_angle,
                                        max_millerindex,
                                        self.general_diff_rules,
                                        self.crystal, 
                                        self.crystal1])
                    
                    ### include slightly misoriented two crystals of different materails
                    seednumber = np.random.randint(1e6)
                    values.append([1, 1, material_,material1_,
                                        self.emin, self.emax, detectorparameters,
                                        pixelsize,True,
                                        ang_maxx, step,
                                        classhkl, classhkl1,
                                        noisy_data, 
                                        remove_peaks,
                                        seednumber,
                                        hkl_all_class,
                                        lattice_material,
                                        None,
                                        normal_hkl,
                                        index_hkl, 
                                        hkl_all_class1,
                                        lattice_material1,
                                        None,
                                        normal_hkl1,
                                        index_hkl1, 
                                        dim1, dim2,
                                        removeharmonics,
                                        3, i, i, save_directory_,
                                        None, None, self.modelp,
                                        self.misorientation_angle,
                                        max_millerindex,
                                        self.general_diff_rules,
                                        self.crystal, 
                                        self.crystal1])
                    
            chunks = chunker_list(values, self.ncpu)
            chunks_mp = list(chunks)

            meta = {'t1':time.time(),
                    'flag':1}
            for ijk in range(int(self.ncpu)):
                self._inputs_queue.put((chunks_mp[ijk], self.ncpu, meta))
                
        self.max_progress = max_progress
        while True:
            count = 0
            for i in range(self.ncpu):
                if not self._worker_process[i].is_alive():
                    self._worker_process[i].join()
                    count += 1
                else:
                    time.sleep(0.1)
                    self.progress.setValue(self.update_progress)
                    QApplication.processEvents()
                    
            if count == self.ncpu:
                self.progress.setValue(self.max_progress)
                QApplication.processEvents()
                return
        
    def update_data_mp(self):
        if not self._outputs_queue.empty():
            self.timermp.blockSignals(True)
            r_message = self._outputs_queue.get()
            self.update_progress = self.update_progress + r_message
            self.timermp.blockSignals(False)

    def generate_training_data(self):
        ### using MP libraries
        self.ncpu = cpu_count_user
        self.write_to_console("Using Multiprocessing ("+str(self.ncpu)+" cpus) for generation of simulated Laue patterns for training", to_push=1)
        self._inputs_queue = Queue()
        self._outputs_queue = Queue()
        ## Update data from multiprocessing
        self.update_progress = 0
        self.max_progress = 0
        self.timermp = QtCore.QTimer()
        self.timermp.setInterval(100) ## check every second (update the list of files in folder)
        self.timermp.timeout.connect(self.update_data_mp)
        self.timermp.start()
        
        self.write_to_console("Generating training dataset", to_push=1)
        self.status.showMessage("Training dataset generation in progress!")
        
        if self.input_params["hkl_max_identify"] == "auto" and self.input_params["hkl_max_identify1"] != "auto":
            self.write_to_console("Calculating the HKL bounds for training dataset", to_push=1)
            self.n, _ = self.temp_HKL(removeharmonics=1)
        elif self.input_params["hkl_max_identify"] == "auto" and self.input_params["hkl_max_identify1"] == "auto":
            self.write_to_console("Calculating the HKL bounds for training dataset", to_push=1)
            self.n, self.n1 = self.temp_HKL(removeharmonics=1)
        elif self.input_params["hkl_max_identify"] != "auto" and self.input_params["hkl_max_identify1"] == "auto":
            self.write_to_console("Calculating the HKL bounds for training dataset", to_push=1)
            _, self.n1 = self.temp_HKL(removeharmonics=1)
            
        ## generate reference HKL library      
        self.write_to_console("Directory for training dataset is : "+self.save_directory)
        ## procedure for generation of GROUND TRUTH classes
        # =============================================================================
        # VERY IMPORTANT; TAKES Significant time; verify again for other symmetries
        # =============================================================================
        self.run_(self.n, self.rules, self.lattice_material, self.symmetry, self.material_, self.crystal, self.SG, self.general_diff_rules)
        if self.material_ != self.material1_:
            self.run_(self.n1, self.rules1, self.lattice_material1, self.symmetry1, self.material1_, self.crystal1, self.SG1, self.general_diff_rules1)
        
        ############ GENERATING TRAINING DATA  
        self.update_progress = 0
        self.max_progress = 0
        self.load_dataset(material_=self.material_, material1_=self.material1_, ang_maxx=self.maximum_angle_to_search,
                          step=self.step_for_binning, mode=self.mode_of_analysis, 
                          nb_grains=self.nb_grains_per_lp,
                          grains_nb_simulate=self.grains_nb_simulate,
                          data_realism = True, detectorparameters=self.detectorparameters, 
                          pixelsize=self.pixelsize, type_="training_data", var0=1,
                          dim1=self.input_params["dim1"], dim2=self.input_params["dim2"], removeharmonics=1)
        # ############ GENERATING TESTING DATA
        self.update_progress = 0
        self.max_progress = 0
        self.load_dataset(material_=self.material_, material1_=self.material1_, ang_maxx=self.maximum_angle_to_search,
                          step=self.step_for_binning, mode=self.mode_of_analysis, 
                          nb_grains=self.nb_grains_per_lp,
                          grains_nb_simulate=self.grains_nb_simulate//self.factor,
                          data_realism = True, detectorparameters=self.detectorparameters, 
                          pixelsize=self.pixelsize, type_="testing_data", var0=0,
                          dim1=self.input_params["dim1"], dim2=self.input_params["dim2"], removeharmonics=1)
        
        ## write MTEX data with training orientation
        try:
            write_training_testing_dataMTEX(self.save_directory,self.material_,self.material1_,
                                            self.lattice_material,self.lattice_material1,
                                            material0_lauegroup, material1_lauegroup)
        except:
            print("Error writing the MTEX file of training and testing data")
            self.write_to_console("Error writing the MTEX file of training and testing data")
        
        self.status.showMessage("Training dataset generation completed with multi CPUs!")
        
        self.rmv_freq_class(freq_rmv=self.freq_rmv, elements=self.elements,
                            freq_rmv1=self.freq_rmv1, elements1=self.elements1)
        self.write_to_console("See the class occurances above and choose appropriate frequency removal parameter to train quickly the network by having few output classes!, if not continue as it is.")
        self.write_to_console("Press Train network button to Train")
        self.train_nn.setEnabled(True)
        self.timermp.stop()
        
    def train_neural_network(self,):
        self.status.showMessage("Neural network training in progress!")
        self.train_nn.setEnabled(False)
        self.rmv_freq_class(freq_rmv=self.freq_rmv, elements=self.elements,
                            freq_rmv1=self.freq_rmv1, elements1=self.elements1)
        self.classhkl = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
        self.angbins = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
        self.loc_new = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_2"]
        with open(self.save_directory+"//class_weights.pickle", "rb") as input_file:
            class_weights = cPickle.load(input_file)
        self.class_weights = class_weights[0]
        ## load model and train
        self.model = self.model_arch_general(len(self.angbins)-1, len(self.classhkl),
                                             kernel_coeff= self.kernel_coeff, bias_coeff=self.bias_coeff, 
                                             lr=self.learning_rate)
        self.train_model()
        self.trialtoolbar1.setEnabled(True)
        self.predict_lnn.setEnabled(True)
        self.status.showMessage("Neural network training completed!")
      
    def train_model(self, prefix="", tag = 0):
        if tag == 2:
            ## retraining from file
            try:
                self.classhkl = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
                self.angbins = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
                self.loc_new = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_2"]
                with open(self.save_directory+"//class_weights.pickle", "rb") as input_file:
                    class_weights = cPickle.load(input_file)
                self.class_weights = class_weights[0]
                ## need to compile again if loaded from file, better to just call the class, if architecture is same
                self.write_to_console("Constructing model")
                self.model = self.model_arch_general(len(self.angbins)-1, len(self.classhkl),
                                                     kernel_coeff= self.kernel_coeff, bias_coeff=self.bias_coeff, 
                                                     lr=self.learning_rate)
                list_of_files = glob.glob(self.save_directory+'//*.h5')
                latest_file = max(list_of_files, key=os.path.getctime)
                self.write_to_console("Taking the latest Weight file from the Folder: " + latest_file)
                load_weights = latest_file
                self.model.load_weights(load_weights)
                self.write_to_console("Uploading weights to model")
                self.write_to_console("All model files found and loaded")
            except:
                self.write_to_console("Model directory is not proper or files are missing. please configure the params")
                return

        ## temp function to quantify the spots and classes present in a batch
        batch_size = self.input_params["batch_size"] 
        trainy_inbatch = self.array_generator_verify(self.save_directory+"//training_data", batch_size, len(self.classhkl), self.loc_new)
        self.write_to_console("Number of spots in a batch of %i files : %i" %(batch_size, len(trainy_inbatch)))
        self.write_to_console("Min, Max class ID is %i, %i" %(np.min(trainy_inbatch), np.max(trainy_inbatch)))
        # try varying batch size and epochs
        epochs = self.input_params["epochs"] 
        ## Batch loading for numpy grain files (Keep low value to avoid overcharging the RAM)
        if self.material_ != self.material1_:
            nb_grains_list = list(range(self.nb_grains_per_lp+1))
            nb_grains1_list = list(range(self.nb_grains_per_lp1+1))
            list_permute = list(itertools.product(nb_grains_list, nb_grains1_list))
            list_permute.pop(0)
            steps_per_epoch = (len(list_permute) * self.grains_nb_simulate)//batch_size
        else:
            steps_per_epoch = int((self.nb_grains_per_lp * self.grains_nb_simulate) / batch_size)
            
        val_steps_per_epoch = int(steps_per_epoch / self.factor)
        if steps_per_epoch == 0:
            steps_per_epoch = 1
        if val_steps_per_epoch == 0:
            val_steps_per_epoch = 1   
        ## Load generator objects from filepaths
        training_data_generator = self.array_generator(self.save_directory+"//training_data", batch_size, len(self.classhkl), self.loc_new)
        testing_data_generator = self.array_generator(self.save_directory+"//testing_data", batch_size, len(self.classhkl), self.loc_new)
        ######### TRAIN THE DATA
        self.progress.setMaximum(epochs*steps_per_epoch)
        # from clr_callback import CyclicLR
        # clr = CyclicLR(base_lr=0.0005, max_lr=0.001, step_size=steps_per_epoch*5, mode='triangular')
        es = EarlyStopping(monitor='val_accuracy', mode='max', patience=5)
        # es = EarlyStopping(monitor='categorical_crossentropy', patience=5)
        ms = ModelCheckpoint(self.save_directory+"//best_val_acc_model.h5", monitor='val_accuracy', mode='max', save_best_only=True)
        
        # model save directory and filename
        if self.material_ != self.material1_:
            model_name = self.save_directory+"//model_"+self.material_+"_"+self.material1_+prefix
        else:
            model_name = self.save_directory+"//model_"+self.material_+prefix
            
        log = LoggingCallback(self.write_to_console, self.progress, QApplication, self.model, model_name)

        stats_model = self.model.fit(
                                    training_data_generator, 
                                    epochs=epochs, 
                                    steps_per_epoch=steps_per_epoch,
                                    validation_data=testing_data_generator,
                                    validation_steps=val_steps_per_epoch,
                                    verbose=1,
                                    class_weight=self.class_weights,
                                    callbacks=[es, ms, log] # es, ms, clr
                                    )
        
        self.progress.setValue(epochs*steps_per_epoch)
        QApplication.processEvents() 
        # Save model config and weightsp
        if tag == 0:
            ## new trained model, save files
            model_json = self.model.to_json()
            with open(model_name+".json", "w") as json_file:
                json_file.write(model_json)            
        # serialize weights to HDF5
        self.model.save_weights(model_name+".h5")
        self.write_to_console("Saved model to disk")

        self.write_to_console( "Training Accuracy: "+str( stats_model.history['accuracy'][-1]))
        self.write_to_console( "Training Loss: "+str( stats_model.history['loss'][-1]))
        self.write_to_console( "Validation Accuracy: "+str( stats_model.history['val_accuracy'][-1]))
        self.write_to_console( "Validation Loss: "+str( stats_model.history['val_loss'][-1]))
        
        epochs = range(1, len(self.model.history.history['loss']) + 1)
        fig, ax = plt.subplots(1,2)
        ax[0].plot(epochs, self.model.history.history['loss'], 'r', label='Training loss')
        ax[0].plot(epochs, self.model.history.history['val_loss'], 'r', ls="dashed", label='Validation loss')
        ax[0].legend()
        ax[1].plot(epochs, self.model.history.history['accuracy'], 'g', label='Training Accuracy')
        ax[1].plot(epochs, self.model.history.history['val_accuracy'], 'g', ls="dashed", label='Validation Accuracy')
        ax[1].legend()
        if self.material_ != self.material1_:
            plt.savefig(self.save_directory+"//loss_accuracy_"+self.material_+"_"+self.material1_+prefix+".png", bbox_inches='tight',format='png', dpi=1000)
        else:
            plt.savefig(self.save_directory+"//loss_accuracy_"+self.material_+prefix+".png", bbox_inches='tight',format='png', dpi=1000)
        plt.close()
        
        if self.material_ != self.material1_:
            text_file = open(self.save_directory+"//loss_accuracy_logger_"+self.material_+"_"+self.material1_+prefix+".txt", "w")
        else:
            text_file = open(self.save_directory+"//loss_accuracy_logger_"+self.material_+prefix+".txt", "w")

        text_file.write("# EPOCH, LOSS, VAL_LOSS, ACCURACY, VAL_ACCURACY" + "\n")
        for inj in range(len(epochs)):
            string1 = str(epochs[inj]) + ","+ str(self.model.history.history['loss'][inj])+\
                    ","+str(self.model.history.history['val_loss'][inj])+","+str(self.model.history.history['accuracy'][inj])+\
                    ","+str(self.model.history.history['val_accuracy'][inj])+" \n"  
            text_file.write(string1)
        text_file.close()
        
        x_test, y_test = self.vali_array(self.save_directory+"//testing_data", 50, len(self.classhkl), self.loc_new)
        y_test = np.argmax(y_test, axis=-1)
        y_pred = np.argmax(self.model.predict(x_test), axis=-1)
        self.write_to_console(classification_report(y_test, y_pred))
        self.write_to_console( "Training is Completed; You can use the Retrain function to run for more epoch with varied batch size")
        self.write_to_console( "Training is Completed; You can use the Prediction and Live Prediction module now")
      
    def rmv_freq_class(self, freq_rmv = 0, elements="all", freq_rmv1 = 0, elements1="all"):
        classhkl0 = np.load(self.save_directory+"//grain_classhkl_angbin.npz")["arr_0"]
        self.write_to_console("First material index length: " + str(len(classhkl0)))
        ind_mat = np.array([ij for ij in range(len(classhkl0))])
        
        if self.material_ != self.material1_:
            classhkl1 = np.load(self.save_directory+"//grain_classhkl_angbin1.npz")["arr_0"]
            self.write_to_console("Second material index length: " + str(len(classhkl1)))
            pre_ind = ind_mat[-1] + 1
            ind_mat1 = np.array([pre_ind+ij for ij in range(len(classhkl1))])
            classhkl = np.vstack((classhkl0, classhkl1))
        else:
            classhkl = classhkl0
            # ind_mat = None
            ind_mat1 = None     
            elements1 = "all"
            freq_rmv1 = 0
        
        angbins = np.load(self.save_directory+"//grain_classhkl_angbin.npz")["arr_1"]
        loc = np.array([ij for ij in range(len(classhkl))])
        trainy_ = self.array_generatorV2(self.save_directory+"//training_data", ver=0)
        
        if self.material_ != self.material1_:
            ## split trainy_ for two materials index
            trainy_mat0 = []
            trainy_mat1 = []
            for ijnode in trainy_:
                if ijnode in ind_mat:
                    trainy_mat0.append(ijnode)
                elif ijnode in ind_mat1:
                    trainy_mat1.append(ijnode)
            trainy_mat0 = np.array(trainy_mat0)
            trainy_mat1 = np.array(trainy_mat1)
        else:
            trainy_mat0 = trainy_
            trainy_mat1 = None
                    
        self.write_to_console("Class ID and frequency; check for data imbalance and select appropriate LOSS function for training the model")
        
        ## lets extract the least common occuring classes to simply the training dataset
        if elements == "all":
            most_common0 = collections.Counter(trainy_mat0).most_common()
        else:
            most_common0 = collections.Counter(trainy_mat0).most_common()[:elements]
            
        if self.material_ != self.material1_:
            if elements1 =="all":
                most_common1 = collections.Counter(trainy_mat1).most_common()
            else:
                most_common1 = collections.Counter(trainy_mat1).most_common()[:elements1]
        else:
            most_common1 = []
                
        most_common = most_common0 + most_common1       
        print(most_common)

        class_present = [most_common[i][0] for i in range(len(most_common))]
        rmv_indices = []
        count = 0
        for i in loc:
            if i not in class_present:
                rmv_indices.append(i)
            elif i in class_present:
                ind_ = np.where(np.array(class_present)==i)[0]
                ij = most_common[ind_[0]]

                if self.material_ != self.material1_:
                    if (ij[0] in ind_mat) and (ij[1] <= freq_rmv):
                        rmv_indices.append(int(ij[0]))
                    if (ij[0] in ind_mat1) and (ij[1] <= freq_rmv1):
                        rmv_indices.append(int(ij[0]))
                else:
                    if (ij[1] <= freq_rmv):
                        rmv_indices.append(int(ij[0]))
            else:
                self.write_to_console("Something Fishy in Remove Freq Class module")
        
        if self.material_ != self.material1_:
            for i in rmv_indices:
                if i in ind_mat:
                    indd = np.where(ind_mat == i)[0]
                    ind_mat = np.delete(ind_mat, indd, axis=0)
                elif i in ind_mat1:
                    indd = np.where(ind_mat1 == i)[0]
                    ind_mat1 = np.delete(ind_mat1, indd, axis=0)
        else:
            for i in rmv_indices:
                if i in ind_mat:
                    indd = np.where(ind_mat == i)[0]
                    ind_mat = np.delete(ind_mat, indd, axis=0)
                    
        loc_new = np.delete(loc, rmv_indices)

        occurances = [most_common[i][1] for i in range(len(most_common)) if int(most_common[i][0]) in loc_new]
        occurances = np.array(occurances)
        
        class_weight = {}
        class_weight_temp = {}
        count = 0
        for i in loc_new:
            for ij in most_common:
                if int(ij[0]) == i:
                    class_weight[count] = int(np.max(occurances)/ij[1]) ##+99 a quick hack to influence the weights
                    class_weight_temp[int(ij[0])] = int(np.max(occurances)/ij[1])
                    count += 1
        
        for occ in range(len(most_common)):
            if int(most_common[occ][0]) in loc_new:
                if int(most_common[occ][0]) == -100:
                    self.write_to_console("Unclassified HKL (-100); occurance : "+str(most_common[occ][1])+": NN_weights : 0.0")
                else:
                    self.write_to_console("HKL : " +str(classhkl[int(most_common[occ][0])])+"; occurance : "+str(most_common[occ][1])+\
                                          ": NN_weights : "+ str(class_weight_temp[int(most_common[occ][0])]))
        
        self.write_to_console(str(len(rmv_indices))+ " classes removed from the classHKL object [removal frequency: "+str(freq_rmv)+"] (before:"+str(len(classhkl))+", now:"+str(len(classhkl)-len(rmv_indices))+")")
        print(str(len(rmv_indices))+ " classes removed from the classHKL object [removal frequency: "+str(freq_rmv)+"] (before:"+str(len(classhkl))+", now:"+str(len(classhkl)-len(rmv_indices))+")")
                
        classhkl = np.delete(classhkl, rmv_indices, axis=0)
        ## save the altered classHKL object
        if self.material_ != self.material1_:
            np.savez_compressed(self.save_directory+'//MOD_grain_classhkl_angbin.npz', classhkl, angbins, loc_new, 
                                rmv_indices, freq_rmv, len(ind_mat), len(ind_mat1))
        else:
            np.savez_compressed(self.save_directory+'//MOD_grain_classhkl_angbin.npz', classhkl, angbins, loc_new, 
                                rmv_indices, freq_rmv)
        with open(self.save_directory + "//class_weights.pickle", "wb") as output_file:
            cPickle.dump([class_weight], output_file)
        self.write_to_console("Saved class weights data")

    def array_generator(self, path_, batch_size, n_classes, loc_new):
        """
        Assign a new class to data that is removed (to include in the training anyway)
        """
        array_pairs = self.get_path(path_, ver=0)
        random.shuffle(array_pairs)
        zipped = itertools.cycle(array_pairs)
        while True:
            temp_var = False
            for bs in range(batch_size):
                array_path = next(zipped)
                obj = np.load(array_path)
                trainX = obj["arr_0"]
                loc1 = obj["arr_1"]
                
                if len(trainX) == 0 or len(loc1) == 0:
                    self.write_to_console("Skipping File: "+ array_path+"; No data is found")
                    if bs == 0:
                        temp_var = True
                    continue                
                ## remove the non frequent class and rearrange the data
                loc1_new = []
                loc1_new_rmv = []
                for k, i in enumerate(loc1):
                    temp_loc = np.where(loc_new==i)[0]
                    if len(temp_loc) == 1:
                        loc1_new.append(temp_loc)
                    else:
                        loc1_new_rmv.append(k)   
                   
                loc1_new = np.array(loc1_new).ravel()
                loc1_new_rmv = np.array(loc1_new_rmv).ravel() 
                
                if len(trainX) != len(loc1_new):
                    if len(loc1_new_rmv) > 0:
                        trainX = np.delete(trainX, loc1_new_rmv, axis=0) 

                if bs == 0 or temp_var:
                    trainX1 = np.copy(trainX)
                    trainY1 = np.copy(loc1_new)
                else:
                    trainX1 = np.vstack((trainX1, trainX))
                    trainY1 = np.hstack((trainY1, loc1_new))

            ## To normalize the size of one hot encoding
            count = 0
            if np.min(trainY1) != 0:
                trainY1 = np.append(trainY1, 0)
                count += 1
            if np.max(trainY1) != (n_classes-1):
                trainY1 = np.append(trainY1, n_classes-1)
                count += 1
                
            trainY1 = to_categorical(trainY1)
            if count == 1:
                trainY1 = np.delete(trainY1, [len(trainY1)-1] ,axis=0)
            elif count == 2:
                trainY1 = np.delete(trainY1, [len(trainY1)-1,len(trainY1)-2] ,axis=0)
    
            yield trainX1, trainY1
            
    def vali_array(self, path_, batch_size, n_classes, loc_new):
        array_pairs = self.get_path(path_, ver=0)
        random.shuffle(array_pairs)
        zipped = itertools.cycle(array_pairs)
        temp_var = False
        for bs in range(batch_size):
            array_path = next(zipped)
            obj = np.load(array_path)
            trainX = obj["arr_0"]
            loc1 = obj["arr_1"]
            
            if len(trainX) == 0 or len(loc1) == 0:
                self.write_to_console("Skipping File: "+ array_path+"; No data is found")
                if bs == 0:
                    temp_var = True
                continue
            
            ## remove the non frequent class and rearrange the data
            loc1_new = []
            loc1_new_rmv = []
            for k, i in enumerate(loc1):
                temp_loc = np.where(loc_new==i)[0]
                if len(temp_loc) == 1:
                    loc1_new.append(temp_loc)
                else:
                    loc1_new_rmv.append(k)
            
            loc1_new = np.array(loc1_new).ravel()
            loc1_new_rmv = np.array(loc1_new_rmv).ravel()
            
            if len(trainX) != len(loc1_new):
                if len(loc1_new_rmv) > 0:
                    trainX = np.delete(trainX, loc1_new_rmv, axis=0)
                
            if bs == 0 or temp_var:
                trainX1 = trainX
                trainY1 = loc1_new
            else:
                trainX1 = np.vstack((trainX1, trainX))
                trainY1 = np.hstack((trainY1, loc1_new))
        
        count = 0
        if np.min(trainY1) != 0:
            trainY1 = np.append(trainY1, 0)
            count += 1
        if np.max(trainY1) != (n_classes-1):
            trainY1 = np.append(trainY1, n_classes-1)
            count += 1
            
        trainY1 = to_categorical(trainY1)
        if count == 1:
            trainY1 = np.delete(trainY1, [len(trainY1)-1] ,axis=0)
        elif count == 2:
            trainY1 = np.delete(trainY1, [len(trainY1)-1,len(trainY1)-2] ,axis=0)
    
        return trainX1, trainY1

    def get_path(self, path_, ver=0):
        image_files = []
        for dir_entry in os.listdir(path_):
            if os.path.isfile(os.path.join(path_, dir_entry)) and \
                    os.path.splitext(dir_entry)[1] in ACCEPTABLE_FORMATS:
                file_name, file_extension = os.path.splitext(dir_entry)
                image_files.append((file_name, file_extension,
                                    os.path.join(path_, dir_entry)))
        return_value = []
        for image_file, _, image_full_path in image_files:
            if image_file == "grain_classhkl_angbin":
                continue
            if image_file == "grain_classhkl_angbin1":
                continue
            if ver == 1 and image_file == "grain_init":
                continue
            if ver == 1 and image_file == "grain_init1":
                continue
            return_value.append((image_full_path))
        return return_value
    
    def array_generator_verify(self, path_, batch_size, n_classes, loc_new):
        array_pairs = self.get_path(path_, ver=1)
        random.shuffle(array_pairs)
        zipped = itertools.cycle(array_pairs)
        while True:
            temp_var = False
            for bs in range(batch_size):
                array_path = next(zipped)
                obj = np.load(array_path)
                loc1 = obj["arr_1"]            
                if len(loc1) == 0:
                    self.write_to_console("Skipping File: "+ array_path+"; No data is found")
                    if bs == 0:
                        temp_var = True
                    continue             
                ## remove the non frequent class and rearrange the data
                loc1_new = []
                for k, i in enumerate(loc1):
                    temp_loc = np.where(loc_new==i)[0]
                    if len(temp_loc) == 1:
                        loc1_new.append(temp_loc)     
                loc1_new = np.array(loc1_new).ravel()
                if bs == 0 or temp_var:
                    trainY1 = np.copy(loc1_new)
                else:
                    trainY1 = np.hstack((trainY1, loc1_new)) 
            return trainY1
    
    def array_generatorV2(self, path_, ver=1):
        array_pairs = self.get_path(path_, ver=ver)
        random.shuffle(array_pairs)
        self.progress.setMaximum(len(array_pairs))
        for bs in range(len(array_pairs)):
            loc1 = np.load(array_pairs[bs])["arr_1"]           
            if bs == 0:
                trainY1 = loc1
            if bs > 0:
                trainY1 = np.hstack((trainY1, loc1))
            self.progress.setValue(bs+1)
            QApplication.processEvents() 
        return trainY1
    
    def model_arch_general(self, n_bins, n_outputs, kernel_coeff = 0.0005, bias_coeff = 0.0005, lr=None, verbose=1):
        """
        Very simple and straight forward Neural Network with few hyperparameters
        straighforward RELU activation strategy with cross entropy to identify the HKL
        Tried BatchNormalization --> no significant impact
        Tried weighted approach --> not better for HCP
        Trying Regularaization 
        l2(0.001) means that every coefficient in the weight matrix of the layer 
        will add 0.001 * weight_coefficient_value**2 to the total loss of the network
        """
        if n_outputs >= n_bins:
            param = n_bins
            if param*15 < (2*n_outputs): ## quick hack; make Proper implementation
                param = (n_bins + n_outputs)//2
        else:
            # param = n_outputs ## More reasonable ???
            param = n_outputs*2 ## More reasonable ???
            # param = n_bins//2
            
        model = Sequential()
        model.add(keras.Input(shape=(n_bins,)))
        ## Hidden layer 1
        model.add(Dense(n_bins, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.3)) ## Adding dropout as we introduce some uncertain data with noise
        ## Hidden layer 2
        model.add(Dense(((param)*15 + n_bins)//2, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.3))
        ## Hidden layer 3
        model.add(Dense((param)*15, kernel_regularizer=l2(kernel_coeff), bias_regularizer=l2(bias_coeff)))
        # model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(0.3))
        ## Output layer 
        model.add(Dense(n_outputs, activation='softmax'))
        ## Compile model
        if lr != None:
            otp = tf.keras.optimizers.Adam(learning_rate=lr)
            model.compile(loss='categorical_crossentropy', optimizer=otp, metrics=[metricsNN])
        else:
            model.compile(loss='categorical_crossentropy', optimizer="adam", metrics=[metricsNN])
        
        if verbose == 1:
            model.summary()
            stringlist = []
            model.summary(print_fn=lambda x: stringlist.append(x))
            short_model_summary = "\n".join(stringlist)
            self.write_to_console(short_model_summary)
        return model
    
    def grid_search_hyperparams(self,): 
        classhkl = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
        angbins = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
        loc_new = np.load(self.save_directory+"//MOD_grain_classhkl_angbin.npz")["arr_2"]
        with open(self.save_directory+"//class_weights.pickle", "rb") as input_file:
            class_weights = cPickle.load(input_file)
        class_weights = class_weights[0]
        
        batch_size = self.input_params["batch_size"] 
        trainy_inbatch = self.array_generator_verify(self.save_directory+"//training_data", batch_size, len(classhkl), loc_new)
        self.write_to_console("Number of spots in a batch of %i files : %i" %(batch_size, len(trainy_inbatch)))
        self.write_to_console("Min, Max class ID is %i, %i" %(np.min(trainy_inbatch), np.max(trainy_inbatch)))
        self.write_to_console("Starting hypergrid optimization: looking in a grid to optimize the learning rate and regularization coefficients.")
        # try varying batch size and epochs
        epochs = 1 #self.input_params["epochs"] 
        ## Batch loading for numpy grain files (Keep low value to avoid overcharging the RAM)
        steps_per_epoch = int((self.nb_grains_per_lp * self.grains_nb_simulate)/batch_size)
        val_steps_per_epoch = int(steps_per_epoch /self.factor)
        if steps_per_epoch == 0:
            steps_per_epoch = 1
        if val_steps_per_epoch == 0:
            val_steps_per_epoch = 1
        ## Load generator objects from filepaths
        training_data_generator = self.array_generator(self.save_directory+"//training_data", batch_size, len(classhkl), loc_new)
        testing_data_generator = self.array_generator(self.save_directory+"//testing_data", batch_size, len(classhkl), loc_new)

        # grid search values
        values = [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6]
        
        all_train, all_test = list(), list()
        all_trainL, all_testL = list(), list()
        parameters = list()
        
        text_file = open(self.save_directory+"//parameter_hypergrid_"+self.material_+".txt", "w")
        text_file.write("# Iter, Learning_Rate, Bias_Coeff, Kernel_Coeff, Train_Acc, Train_Loss, Test_Acc, Test_Loss, LR_index, BC_index, KC_index" + "\n")
        
        self.progress.setMaximum(len(values)*len(values)*len(values))

        iter_cnt= 0 
        for i, param in enumerate(values):
            for j, param1 in enumerate(values):
                for k, param2 in enumerate(values):
                        # define model
                    iter_cnt += 1

                    model = self.model_arch_general(len(angbins)-1, len(classhkl), 
                                                       kernel_coeff = param2, 
                                                       bias_coeff = param1,
                                                       lr = param, verbose=0)
                        # fit model
                    stats_model = model.fit(
                                            training_data_generator, 
                                            epochs=epochs, 
                                            steps_per_epoch=steps_per_epoch,
                                            validation_data=testing_data_generator,
                                            validation_steps=val_steps_per_epoch,
                                            verbose=0,
                                            class_weight=class_weights,
                                            )
    
                        # evaluate the model
                    train_acc = stats_model.history['accuracy'][-1]
                    test_acc = stats_model.history['val_accuracy'][-1]
                    train_loss = stats_model.history['loss'][-1]
                    test_loss = stats_model.history['val_loss'][-1]
                    all_train.append(train_acc)
                    all_test.append(test_acc)
                    all_trainL.append(train_loss)
                    all_testL.append(test_loss)
                    parameters.append([param,param1,param2])
                    
                    string1 = str(iter_cnt) +","+ str(param) + ","+ str(param1)+\
                                ","+str(param2)+","+str(train_acc)+\
                                ","+str(train_loss)+ ","+str(test_acc)+","+str(test_loss)+","+ str(i) + ","+ str(j)+\
                                    ","+str(k)+ " \n"  
                    text_file.write(string1)                  
                    self.progress.setValue(iter_cnt)
                    QApplication.processEvents()         
        text_file.close()
    
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, subplot=1, mat_bool=True):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        if mat_bool:
            self.axes = self.fig.add_subplot(131)
            self.axes1 = self.fig.add_subplot(132)
            self.axes2 = self.fig.add_subplot(133)
        else:
            self.axes = self.fig.add_subplot(141)
            self.axes1 = self.fig.add_subplot(142)
            self.axes2 = self.fig.add_subplot(143)
            self.axes3 = self.fig.add_subplot(144)
        super(MplCanvas, self).__init__(self.fig)

class MplCanvas1(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas1, self).__init__(self.fig)

class MyPopup_image(QWidget):
    def __init__(self, th_exp, chi_exp, intensity, tth_sim, chi_sim, ix, iy, file, exp_linkspots, residues, theo_index):
        QWidget.__init__(self)
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        self.layout = QVBoxLayout() # QGridLayout()
        self.canvas = MplCanvas1(self, width=10, height=10, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # set the layout
        self.layout.addWidget(self.toolbar, 0)
        self.layout.addWidget(self.canvas, 100)
        self.setLayout(self.layout)
        # Drop off the first y element, append a new one.
        intensity = 10 #intensity / np.amax(intensity) * 100.0
        self.canvas.axes.cla()
        self.canvas.axes.set_title("Laue pattern of pixel x=%d, y=%d (file: %s)"%(iy,ix,file), loc='center', fontsize=8)
        self.canvas.axes.scatter(th_exp*2.0, chi_exp, c='k', s=intensity, label="Exp spots")
        self.canvas.axes.scatter(tth_sim, chi_sim, facecolor='none', edgecolor='r', label="Best match spots")
        # Trigger the canvas to update and redraw.
        self.canvas.axes.grid(True)
        self.canvas.axes.legend(fontsize=8)
        self.canvas.draw()

        self._createDisplay() ## display screen
        ##create a text string to display
        texttstr = "# Total experimental spots : "+str(len(th_exp))
        self.setDisplayText(texttstr)
        texttstr = "# Average residues : "+str(np.average(residues))
        self.setDisplayText(texttstr)
        texttstr = "# Total linked spots : "+str(len(exp_linkspots))
        self.setDisplayText(texttstr)
        texttstr = "# Matching rate : "+str(len(exp_linkspots)/len(tth_sim))
        self.setDisplayText(texttstr)
        
        texttstr = "# Simulated_spots\tExperimental_spots\tResidues\t "
        self.setDisplayText(texttstr)
        for i in range(len(theo_index)):
            texttstr = str(theo_index[i])+"\t"+str(exp_linkspots[i])+"\t"+str(residues[i])
            self.setDisplayText(texttstr)

    def _createDisplay(self):
        """Create the display."""
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.append('%s'%text)
        self.display.moveCursor(QtGui.QTextCursor.Start)
        self.display.setFocus()
        
class sample_config(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self._createDisplay() ## display screen
        self.setDisplayText(texttstr)

    def _createDisplay(self):
        """Create the display."""
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.append('%s'%text)
        self.display.moveCursor(QtGui.QTextCursor.End)
        self.display.setFocus()
        
class MyPopup(QWidget):
    def __init__(self, match_rate12, rotation_matrix12, mat_global12, fR_pix12, filename, 
                 straincrystal, strainsample, end_time, 
                 match_rate12fast, rotation_matrix12fast, mat_global12fast, fR_pix12fast, 
                 straincrystalfast, strainsamplefast, end_timefast,
                 match_rate12beamtime, rotation_matrix12beamtime, mat_global12beamtime, fR_pix12beamtime, 
                 straincrystalbeamtime, strainsamplebeamtime, end_timebeamtime,
                  match_rate12multiorimat, rotation_matrix12multiorimat, mat_global12multiorimat, fR_pix12multiorimat, 
                  straincrystalmultiorimat, strainsamplemultiorimat, end_timemultiorimat):
        QWidget.__init__(self)
        
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self._createDisplay() ## display screen

        texttstr = "Predicted for File: "+filename+ " \n" 
        self.setDisplayText(texttstr)
        self.setDisplayText("################## SLOW MODE ############### \n")
        for ijk in range(len(match_rate12)):
            self.setDisplayText("--------------- Matrix "+str(ijk+1)+" \n")
            texttstr = "Matching rate for the proposed matrix is: "+str(match_rate12[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            texttstr = "Identified material index is: "+str(mat_global12[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            temp_ = rotation_matrix12[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Rotation matrix is: "+string1
            self.setDisplayText(texttstr)
            temp_ = straincrystal[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain crystal reference frame is: "+string1
            self.setDisplayText(texttstr)
            temp_ = strainsample[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain sample reference frame is: "+string1
            self.setDisplayText(texttstr)
            texttstr = "Final pixel residues is: "+str(fR_pix12[ijk][0]) + " \n"
            self.setDisplayText(texttstr)
            texttstr = "Total time in seconds (Loading image, peak detection, HKL prediction, Orientation matrix computation, strain computation): "+str(end_time) + " \n"
            self.setDisplayText(texttstr)        
        
        self.setDisplayText("################## FAST MODE ############### \n")
        for ijk in range(len(match_rate12fast)):
            self.setDisplayText("--------------- Matrix "+str(ijk+1)+" \n")
            texttstr = "Matching rate for the proposed matrix is: "+str(match_rate12fast[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            texttstr = "Identified material index is: "+str(mat_global12fast[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            temp_ = rotation_matrix12fast[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Rotation matrix is: "+string1
            self.setDisplayText(texttstr)
            temp_ = straincrystalfast[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain crystal reference frame is: "+string1
            self.setDisplayText(texttstr)
            temp_ = strainsamplefast[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain sample reference frame is: "+string1
            self.setDisplayText(texttstr)
            texttstr = "Final pixel residues is: "+str(fR_pix12fast[ijk][0]) + " \n"
            self.setDisplayText(texttstr)
            texttstr = "Total time in seconds (Loading image, peak detection, HKL prediction, Orientation matrix computation, strain computation): "+str(end_timefast) + " \n"
            self.setDisplayText(texttstr)    
            
        self.setDisplayText("################## BEAMTIME MODE ############### \n")
        for ijk in range(len(match_rate12beamtime)):
            self.setDisplayText("--------------- Matrix "+str(ijk+1)+" \n")
            texttstr = "Matching rate for the proposed matrix is: "+str(match_rate12beamtime[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            texttstr = "Identified material index is: "+str(mat_global12beamtime[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            temp_ = rotation_matrix12beamtime[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Rotation matrix is: "+string1
            self.setDisplayText(texttstr)
            temp_ = straincrystalbeamtime[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain crystal reference frame is: "+string1
            self.setDisplayText(texttstr)
            temp_ = strainsamplebeamtime[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain sample reference frame is: "+string1
            self.setDisplayText(texttstr)
            texttstr = "Final pixel residues is: "+str(fR_pix12beamtime[ijk][0]) + " \n"
            self.setDisplayText(texttstr)
            texttstr = "Total time in seconds (Loading image, peak detection, HKL prediction, Orientation matrix computation, strain computation): "+str(end_timebeamtime) + " \n"
            self.setDisplayText(texttstr)    
            
        self.setDisplayText("################## GRAPHMODE MODE ############### \n")
        for ijk in range(len(match_rate12multiorimat)):
            self.setDisplayText("--------------- Matrix "+str(ijk+1)+" \n")
            texttstr = "Matching rate for the proposed matrix is: "+str(match_rate12multiorimat[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            texttstr = "Identified material index is: "+str(mat_global12multiorimat[ijk][0])+ " \n" 
            self.setDisplayText(texttstr)
            temp_ = rotation_matrix12multiorimat[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Rotation matrix is: "+string1
            self.setDisplayText(texttstr)
            temp_ = straincrystalmultiorimat[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain crystal reference frame is: "+string1
            self.setDisplayText(texttstr)
            temp_ = strainsamplemultiorimat[ijk][0].flatten()
            string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                        "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                            "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
            texttstr = "Strain sample reference frame is: "+string1
            self.setDisplayText(texttstr)
            texttstr = "Final pixel residues is: "+str(fR_pix12multiorimat[ijk][0]) + " \n"
            self.setDisplayText(texttstr)
            texttstr = "Total time in seconds (Loading image, peak detection, HKL prediction, Orientation matrix computation, strain computation): "+str(end_timemultiorimat) + " \n"
            self.setDisplayText(texttstr)
            
    def _createDisplay(self):
        """Create the display."""
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.layout.addWidget(self.display)

    def setDisplayText(self, text):
        self.display.append('%s'%text)
        self.display.moveCursor(QtGui.QTextCursor.End)
        self.display.setFocus()

class AnotherWindowParams(QWidget):
    got_signal = QtCore.pyqtSignal(dict)
    def __init__(self, state=0, gui_state=0):
        super().__init__()
        
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.settings = QSettings("config_data_"+str(gui_state),"ConfigGUI_"+str(gui_state))
        ## Material detail        
        self.dict_LT = QComboBox()
        sortednames = sorted(dictLT.dict_Materials.keys(), key=lambda x:x.lower())
        for s in sortednames:
            self.dict_LT.addItem(s)
        
        self.dict_LT1 = QComboBox()
        sortednames = sorted(dictLT.dict_Materials.keys(), key=lambda x:x.lower())
        for s in sortednames:
            self.dict_LT1.addItem(s)
        
        if main_directory != None:
            self.modelDirecSave = main_directory
        else:
            self.modelDirecSave = None
        self.model_direc_save = QPushButton('Browse')
        self.model_direc_save.clicked.connect(self.getfiles)
        
        self.symmetry = QComboBox()
        symmetry_names = ["cubic","hexagonal","orthorhombic","tetragonal","trigonal","monoclinic","triclinic"]
        for s in symmetry_names:
            self.symmetry.addItem(s)
        
        self.symmetry1 = QComboBox()
        symmetry_names = ["cubic","hexagonal","orthorhombic","tetragonal","trigonal","monoclinic","triclinic"]
        for s in symmetry_names:
            self.symmetry1.addItem(s)
        
        self.prefix = QLineEdit()
        self.prefix.setText("") ## Prefix for folder
        
        self.hkl_max = QLineEdit()
        self.hkl_max.setText("auto") ## auto or some indices of HKL
        
        self.elements = QLineEdit()
        self.elements.setText("200") ## all or some length
        
        self.freq_rmv = QLineEdit()
        self.freq_rmv.setText("1") ## auto or some indices of HKL
        
        self.hkl_max1 = QLineEdit()
        self.hkl_max1.setText("auto") ## auto or some indices of HKL
        
        self.elements1 = QLineEdit()
        self.elements1.setText("200") ## all or some length
        
        self.freq_rmv1 = QLineEdit()
        self.freq_rmv1.setText("1") ## auto or some indices of HKL
        
        self.maximum_angle_to_search = QLineEdit()
        self.maximum_angle_to_search.setText("90")
        
        self.step_for_binning = QLineEdit()
        self.step_for_binning.setText("0.1")
        
        self.mode_of_analysis = QComboBox()
        mode_ = ["1","0"]
        for s in mode_:
            self.mode_of_analysis.addItem(s)
            
        self.nb_grains_per_lp = QLineEdit()
        self.nb_grains_per_lp.setText("5")
        
        self.nb_grains_per_lp1 = QLineEdit()
        self.nb_grains_per_lp1.setText("5")
        
        self.grains_nb_simulate = QLineEdit()
        self.grains_nb_simulate.setText("500")
        
        self.detectordistance = QLineEdit()
        self.detectordistance.setText("79.553")
        
        self.xycenter = QLineEdit()
        self.xycenter.setText("979.32,932.31")
        
        self.bgdetector = QLineEdit()
        self.bgdetector.setText("0.37,0.447")
        
        self.detectordim = QLineEdit()
        self.detectordim.setText("2018,2016")
        
        self.pixelsize = QLineEdit()
        self.pixelsize.setText("0.0734")
        
        self.minmaxE = QLineEdit()
        self.minmaxE.setText("5,18")
        
        self.include_scm = QComboBox()
        modes = ["no", "yes"]
        for s in modes:
            self.include_scm.addItem(s)
            
        self.architecture = QComboBox()
        modes = ["Classical-inbuilt","from file"]
        for s in modes:
            self.architecture.addItem(s)
            
        self.learningrate_rc = QLineEdit()
        self.learningrate_rc.setText("1e-3,1e-5,1e-6")

        self.mode_nn = QComboBox()
        modes = ["Generate Data & Train","Train","Predict"]
        for s in modes:
            self.mode_nn.addItem(s)
        
        self.batch_size = QLineEdit()
        self.batch_size.setText("20")
        
        self.epochs = QLineEdit()
        self.epochs.setText("5")
        
        self.grid_search_hyperparams = QComboBox()
        mode_ = ["False","True"]
        for s in mode_:
            self.grid_search_hyperparams.addItem(s)
            
        self.texture_model = QComboBox()
        mode_ = ["in-built_Uniform_Distribution","random","from file"]
        for s in mode_:
            self.texture_model.addItem(s)
            
        # button to continue training
        self.btn_config = QPushButton('Accept')
        self.btn_config.clicked.connect(self.send_details_mainGUI)
        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.close)

        ### set some default values
        if freq_rmv_global != None:
            self.freq_rmv.setText(str(freq_rmv_global))
        if elements_global != None:
            self.elements.setText(elements_global)
        if hkl_max_global != None:
            self.hkl_max.setText(hkl_max_global)
        if nb_grains_per_lp_global != None:
            self.nb_grains_per_lp.setText(str(nb_grains_per_lp_global))
        
        if freq_rmv1_global != None:
            self.freq_rmv1.setText(str(freq_rmv1_global))
        if elements1_global != None:
            self.elements1.setText(elements1_global)
        if hkl_max1_global != None:
            self.hkl_max1.setText(hkl_max1_global)
        if nb_grains_per_lp1_global != None:
            self.nb_grains_per_lp1.setText(str(nb_grains_per_lp1_global))
            
        if include_scm_global:
            self.include_scm.setCurrentText("yes")
        else:
            self.include_scm.setCurrentText("no")
            
        if batch_size_global != None:
            self.batch_size.setText(str(batch_size_global))
        if epochs_global != None:
            self.epochs.setText(str(epochs_global))  
            
        if maximum_angle_to_search_global != None:
            self.maximum_angle_to_search.setText(str(maximum_angle_to_search_global))
        if step_for_binning_global != None:
            self.step_for_binning.setText(str(step_for_binning_global))
        if grains_nb_simulate_global != None:
            self.grains_nb_simulate.setText(str(grains_nb_simulate_global))    
            
        if symmetry_global != None:
            self.symmetry.setCurrentText(symmetry_global)
        if symmetry1_global != None:
            self.symmetry1.setCurrentText(symmetry1_global)
        if material_global != None:
            self.dict_LT.setCurrentText(material_global)
        if material1_global != None:
            self.dict_LT1.setCurrentText(material1_global)
        if prefix_global != None:
            self.prefix.setText(prefix_global)
        if detectorparameters_global != None:
            self.detectordistance.setText(str(detectorparameters_global[0]))
            self.xycenter.setText(str(detectorparameters_global[1])+","+str(detectorparameters_global[2]))
            self.bgdetector.setText(str(detectorparameters_global[3])+","+str(detectorparameters_global[4]))
            self.detectordim.setText(str(dim1_global)+","+str(dim2_global))
            self.pixelsize.setText(str(pixelsize_global))
            self.minmaxE.setText(str(emin_global)+","+str(emax_global))

        self.layout = QVBoxLayout() # QGridLayout()

        formLayout = QFormLayout()
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('Training parameters', QLineEdit().setReadOnly(True))
        formLayout.addRow('Directory where \n model files are saved', self.model_direc_save)
        formLayout.addRow('Material details', QLineEdit().setReadOnly(True))
        formLayout.addRow('Prefix for save folder', self.prefix)
        formLayout.addRow('Choose Material and Symmetry \n (incase of 1 material, keep both same)', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.dict_LT, self.dict_LT1)
        formLayout.addRow(self.symmetry, self.symmetry1)
        formLayout.addRow('Class removal frequency', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.freq_rmv, self.freq_rmv1)
        formLayout.addRow('Class length', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.elements, self.elements1)
        formLayout.addRow('HKL max probed', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.hkl_max, self.hkl_max1)
        formLayout.addRow('Histogram parameters', QLineEdit().setReadOnly(True))
        formLayout.addRow('Angular distance to probe (in deg)', self.maximum_angle_to_search)
        formLayout.addRow('Angular bin widths (in deg)', self.step_for_binning)
        formLayout.addRow('Simulation parameters', QLineEdit().setReadOnly(True))
        # formLayout.addRow('Analysis mode', self.mode_of_analysis)
        formLayout.addRow('Max Nb. of grain in a LP', QLineEdit().setReadOnly(True))
        formLayout.addRow(self.nb_grains_per_lp, self.nb_grains_per_lp1)
        formLayout.addRow('Nb. of simulations', self.grains_nb_simulate)
        formLayout.addRow('Include single crystal \n misorientation', self.include_scm)
        formLayout.addRow('Detector parameters', QLineEdit().setReadOnly(True))
        formLayout.addRow('Detector distance', self.detectordistance)
        formLayout.addRow('Detector XY center', self.xycenter)
        formLayout.addRow('Detector Beta Gamma', self.bgdetector)
        formLayout.addRow('Detector Pixel size', self.pixelsize)
        formLayout.addRow('Detector dimensions (dim1,dim2)', self.detectordim)
        formLayout.addRow('Energy (Min, Max)', self.minmaxE)
        formLayout.addRow('Neural Network parameters', QLineEdit().setReadOnly(True))
        formLayout.addRow('Mode of analysis', self.mode_nn)
        formLayout.addRow('Model Architecture', self.architecture)
        formLayout.addRow('LR, Regularization coefficient', self.learningrate_rc)
        formLayout.addRow('Batch size', self.batch_size)
        formLayout.addRow('Epochs', self.epochs)
        formLayout.addRow('Grid search for model Params', self.grid_search_hyperparams)
        formLayout.addRow('Texture for data', self.texture_model)
        
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow(close_button, self.btn_config)

        self.layout.addLayout(formLayout)
        self.setLayout(self.layout)
        self._gui_save()
        if state > 0:
            self._gui_restore()
    
    def getfiles(self):
        self.modelDirecSave = QFileDialog.getExistingDirectory(self, 'Select Folder in which model files will be saved')
    
    def _gui_save(self):
      # Save geometry
        for name, obj in inspect.getmembers(self):
          # if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current index from combobox
                text = obj.itemText(index)  # get the text for current index
                self.settings.setValue(name, text)  # save combobox selection to registry
            if isinstance(obj, QLineEdit):
                value = obj.text()
                self.settings.setValue(name, value)  # save ui values, so they can be restored next time
        self.settings.sync()

    def _gui_restore(self):
        # Restore geometry  
        for name, obj in inspect.getmembers(self):
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current region from combobox
                value = (self.settings.value(name))
                if value == "":
                    continue
                index = obj.findText(value)  # get the corresponding index for specified string in combobox
          
                if index == -1:  # add to list if not found
                    obj.insertItems(0, [value])
                    index = obj.findText(value)
                    obj.setCurrentIndex(index)
                else:
                    obj.setCurrentIndex(index)  # preselect a combobox value by index
            if isinstance(obj, QLineEdit):
                value = (self.settings.value(name))#.decode('utf-8'))  # get stored value from registry
                obj.setText(value)  # restore lineEditFile
        self.settings.sync()
        
    def send_details_mainGUI(self):
        self._gui_save()
        detector_params = [float(self.detectordistance.text()),
                           float(self.xycenter.text().split(",")[0]), 
                           float(self.xycenter.text().split(",")[1]),
                           float(self.bgdetector.text().split(",")[0]), 
                           float(self.bgdetector.text().split(",")[1])]
        
        global prefix_global, weightfile_global, modelfile_global, model_weight_file
        if self.prefix.text() != prefix_global:
            prefix_global = self.prefix.text()
            ##exp directory
            if material_global == material1_global:
                fn = material_global + prefix_global
            else:
                fn = material_global + "_" + material1_global + prefix_global
                        
            modelfile_global = self.modelDirecSave + "//" + fn
            if material_global == material1_global:
                if model_weight_file == "none":
                    weightfile_global = modelfile_global + "//" + "model_" + material_global + ".h5"
                else:
                    weightfile_global = model_weight_file
            else:
                if model_weight_file == "none":
                    weightfile_global = modelfile_global + "//" + "model_" + material_global + "_" + material1_global + ".h5"
                else:
                    weightfile_global = model_weight_file
                    
        # create a dictionary and emit the signal
        emit_dictionary = { "material_": self.dict_LT.currentText(), ## same key as used in LaueTools
                            "material1_": self.dict_LT1.currentText(),
                            "prefix": self.prefix.text(),
                            "symmetry": self.symmetry.currentText(),
                            "symmetry1": self.symmetry1.currentText(),
                            "hkl_max_identify" : self.hkl_max.text(), # can be "auto" or an index i.e 12
                            "hkl_max_identify1" : self.hkl_max1.text(), # can be "auto" or an index i.e 12
                            "maximum_angle_to_search" : float(self.maximum_angle_to_search.text()),
                            "step_for_binning" : float(self.step_for_binning.text()),
                            "mode_of_analysis" : int(self.mode_of_analysis.currentText()),
                            "nb_grains_per_lp" : int(self.nb_grains_per_lp.text()), ## max grains to expect in a LP
                            "nb_grains_per_lp1" : int(self.nb_grains_per_lp1.text()),
                            "grains_nb_simulate" : int(self.grains_nb_simulate.text()),
                            "detectorparameters" : detector_params,
                            "pixelsize" : float(self.pixelsize.text()),
                            "dim1":float(self.detectordim.text().split(",")[0]),
                            "dim2":float(self.detectordim.text().split(",")[1]),
                            "emin":float(self.minmaxE.text().split(",")[0]),
                            "emax" : float(self.minmaxE.text().split(",")[1]),
                            "batch_size": int(self.batch_size.text()), ## batches of files to use while training
                            "epochs": int(self.epochs.text()), ## number of epochs for training
                            "texture": self.texture_model.currentText(),
                            "mode_nn": self.mode_nn.currentText(),
                            "grid_bool": self.grid_search_hyperparams.currentText(),
                            "directory": self.modelDirecSave,
                            "freq_rmv": int(self.freq_rmv.text()),
                            "freq_rmv1": int(self.freq_rmv1.text()),
                            "elements": self.elements.text(),
                            "elements1": self.elements1.text(),
                            "include_scm": self.include_scm.currentText(),
                            "lr":float(self.learningrate_rc.text().split(",")[0]),
                            "kc" : float(self.learningrate_rc.text().split(",")[1]),
                            "bc":float(self.learningrate_rc.text().split(",")[0]),
                            }
        self.got_signal.emit(emit_dictionary)
        self.close() # close the window

class AnotherWindowLivePrediction(QWidget):#QWidget QScrollArea
    def __init__(self, state=0, gui_state=0, material_=None, material1_=None, emin=None, emax=None, 
                 symmetry=None, symmetry1=None, detectorparameters=None, pixelsize=None, lattice_=None, 
                 lattice1_=None, hkl_all_class0=None, hkl_all_class1=None, mode_spotCycleglobal=None,
                 softmax_threshold_global = None, mr_threshold_global =    None, cap_matchrate =    None,
                 coeff =    None, coeff_overlap1212 =    None, fit_peaks_gaussian_global =    None,
                 FitPixelDev_global =    None, NumberMaxofFits =    None, tolerance_strain =    None, tolerance_strain1 =    None,
                 material0_limit = None, material1_limit=None, symmetry_name=None, symmetry1_name=None,
                 use_previous_UBmatrix_name = None, material_phase_always_present=None, crystal=None, crystal1=None):
        super(AnotherWindowLivePrediction, self).__init__()
        
        app_icon = QtGui.QIcon()
        app_icon.addFile(Logo, QtCore.QSize(16,16))
        self.setWindowIcon(app_icon)
        
        self.material_phase_always_present = material_phase_always_present
        self.symmetry_name = symmetry_name
        self.symmetry1_name = symmetry1_name
        self.material0_limit = material0_limit
        self.material1_limit = material1_limit
        self.softmax_threshold_global = softmax_threshold_global
        self.mr_threshold_global = mr_threshold_global
        self.cap_matchrate = cap_matchrate
        self.coeff = coeff
        self.coeff_overlap = coeff_overlap1212
        self.fit_peaks_gaussian_global = fit_peaks_gaussian_global
        self.FitPixelDev_global = FitPixelDev_global
        self.NumberMaxofFits = NumberMaxofFits        
        self.tolerance_strain = tolerance_strain
        self.tolerance_strain1 = tolerance_strain1
        self.mode_spotCycle = mode_spotCycleglobal
        self.material_ = material_
        self.material1_ = material1_
        self.files_treated = []
        self.cnt = 0
        self.emin = emin
        self.emax= emax
        self.lattice_ = lattice_
        self.lattice1_ = lattice1_
        self.symmetry = symmetry
        self.symmetry1 = symmetry1
        self.crystal = crystal
        self.crystal1 = crystal1
        self.hkl_all_class0 = hkl_all_class0
        self.hkl_all_class1 = hkl_all_class1
        self.col = np.zeros((10,3))
        self.colx = np.zeros((10,3))
        self.coly = np.zeros((10,3))
        self.match_rate = np.zeros((10,1))
        self.spots_len = np.zeros((10,1))
        self.iR_pix = np.zeros((10,1))
        self.fR_pix = np.zeros((10,1))
        self.mat_global = np.zeros((10,1))
        self.rotation_matrix = np.zeros((10,3,3))
        self.strain_matrix = np.zeros((10,3,3))
        self.strain_matrixs = np.zeros((10,3,3))
        self.strain_calculation = False
        self.cnt_matrix = True   
        self.use_previous_UBmatrix_name = use_previous_UBmatrix_name
        
        self.detectorparameters = detectorparameters
        self.pixelsize= pixelsize

        if expfile_global != None:
            self.filenameDirec = expfile_global
        else:
            self.filenameDirec = None
        self.experimental = QPushButton('Browse')
        self.experimental.clicked.connect(self.getfiles1)
        
        self.ipf_axis = QComboBox()
        choices = ["Z","Y","X"]
        for s in choices:
            self.ipf_axis.addItem(s)
        
        self.filenamebkg = None
        self.filename_bkg = QPushButton('Browse')
        self.filename_bkg.clicked.connect(self.getfilebkg_file)
        
        self.blacklist_file = None
        self.filename_blst = QPushButton('Browse')
        self.filename_blst.clicked.connect(self.getfileblst_file)
        
        self.tolerance = QLineEdit()
        self.tolerance.setText("0.5")
        
        self.tolerance1 = QLineEdit()
        self.tolerance1.setText("0.5")
        
        self.image_grid = QLineEdit()
        self.image_grid.setText("10,10")
        
        self.ubmat = QLineEdit()
        self.ubmat.setText("1")
        
        self.bkg_treatment = QLineEdit()
        self.bkg_treatment.setText("A-B")

        if modelfile_global != None:
            self.modelDirec = modelfile_global
        else:
            self.modelDirec = None
        self.model_direc = QPushButton('Browse')
        self.model_direc.clicked.connect(self.getfiles)

        if weightfile_global != None:
            self.filenameModel = [weightfile_global]
        else: 
            self.filenameModel = None
        self.model_path = QPushButton('Browse')
        self.model_path.clicked.connect(self.getfileModel)
        
        self.ccd_label = QComboBox()
        self.ccd_label.addItem("Cor")
        choices = dictLT.dict_CCD.keys()
        for s in choices:
            self.ccd_label.addItem(s)
            
        self.intensity_threshold = QLineEdit()
        self.intensity_threshold.setText("1500")
        
        self.experimental_prefix = QLineEdit()
        self.experimental_prefix.setText("")
        
        self.boxsize = QLineEdit()
        self.boxsize.setText("5")
        
        self.hkl_plot = QLineEdit()
        self.hkl_plot.setText("[1,1,0],[1,1,1],[1,0,0]")
        
        self.matrix_plot = QComboBox()
        choices = ["1"]
        for s in choices:
            self.matrix_plot.addItem(s)
            
        self.strain_plot = QComboBox()
        choices = ["11_sample","22_sample","33_sample","12_sample","13_sample","23_sample",\
                   "11_crystal","22_crystal","33_crystal","12_crystal","13_crystal","23_crystal"]
        for s in choices:
            self.strain_plot.addItem(s)
        
        self.matrix_plot_tech = QComboBox()
        choices = ["Sequential", "MultiProcessing"]
        for s in choices:
            self.matrix_plot_tech.addItem(s)        
        
        self.analysis_plot_tech = QComboBox()
        choices = ["slow", "fast", "beamtime", "graphmode", "multiorimat"]
        for s in choices:
            self.analysis_plot_tech.addItem(s)
        
        self.strain_plot_tech = QComboBox()
        choices = ["NO", "YES"]
        for s in choices:
            self.strain_plot_tech.addItem(s)
            
        ### default values here
        if tolerance_global != None:
            self.tolerance.setText(str(tolerance_global))
        if tolerance_global1 != None:
            self.tolerance1.setText(str(tolerance_global1))
        if image_grid_globalx != None:
            self.image_grid.setText(str(image_grid_globalx)+","+str(image_grid_globaly))
        if exp_prefix_global != None:
            self.experimental_prefix.setText(exp_prefix_global)
        if ccd_label_global != None:
            self.ccd_label.setCurrentText(ccd_label_global)
        if intensity_threshold_global != None:
            self.intensity_threshold.setText(str(intensity_threshold_global))
        if UB_matrix_global != None:
            self.boxsize.setText(str(boxsize_global))
        if UB_matrix_global != None:
            self.ubmat.setText(str(UB_matrix_global)) 
        if strain_label_global != None:
            self.strain_plot_tech.setCurrentText(strain_label_global)
        if mode_spotCycle != None:
            self.analysis_plot_tech.setCurrentText(mode_spotCycle)
        if hkls_list_global != None:
            self.hkl_plot.setText(hkls_list_global) 
            
        # button to continue training
        self.btn_config = QPushButton('Predict and Plot')
        self.btn_config.clicked.connect(self.plot_pc)
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self.plot_btn_stop)
        self.btn_save = QPushButton("Save data and plots")
        self.btn_save.clicked.connect(self.save_btn)
        self.btn_load = QPushButton("Predict single file")
        self.btn_load.clicked.connect(self.predict_single_file)
        self.btn_stop.setEnabled(False)
        self.btn_save.setEnabled(False)
        
        mat_bool = False
        if self.material_ == self.material1_:
            mat_bool = True
        
        self.layout = QVBoxLayout() # QGridLayout()
        self.canvas = MplCanvas(self, width=10, height=10, dpi=100, mat_bool=mat_bool)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.canvas.fig.canvas.mpl_connect('button_press_event', self.onclickImage)
        
        # set the layout
        self.layout.addWidget(self.toolbar, 0)
        self.layout.addWidget(self.canvas, 100)

        formLayout = QFormLayout()
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow('Image XY grid size',self.image_grid)
        formLayout.addRow('IPF axis (Cubic and HCP system)', self.ipf_axis)
        # formLayout.addRow('Predicition config', QLineEdit().setReadOnly(True))
        # formLayout.addRow('Directory where \n model files are', self.model_direc)
        # formLayout.addRow('Model weights path', self.model_path)
        # formLayout.addRow('Experimental file config', QLineEdit().setReadOnly(True))
        # formLayout.addRow('Experimental Directory', self.experimental)
        # formLayout.addRow('Experimental file prefix', self.experimental_prefix)
        # formLayout.addRow('Experimental static noise', self.filename_bkg)
        # formLayout.addRow('BlackList peaks', self.filename_blst)
        # formLayout.addRow('Background treatment expression', self.bkg_treatment)
        # formLayout.addRow('if peak search required', QLineEdit().setReadOnly(True))
        # formLayout.addRow('CCD label', self.ccd_label)
        # formLayout.addRow('Peak Search Intensity threshold', self.intensity_threshold)
        # formLayout.addRow('Peak Search BOX size', self.boxsize)
        # formLayout.addRow('UB matrix config', QLineEdit().setReadOnly(True))
        # formLayout.addRow('Tolerance angle', self.tolerance)
        formLayout.addRow('Matricies to predict (sequential)', self.ubmat)       
        formLayout.addRow('Matrix to plot', self.matrix_plot) 
        formLayout.addRow('Strain component to plot', self.strain_plot) 
        # formLayout.addRow('Calculate strain (rough)', self.strain_plot_tech) 
        formLayout.addRow('CPU mode', self.matrix_plot_tech) 
        formLayout.addRow('Analysis mode', self.analysis_plot_tech) 
        # formLayout.setVerticalSpacing(5)
        formLayout.addRow(self.btn_stop, self.btn_config)
        formLayout.addRow(self.btn_load, self.btn_save)

        self.layout.addLayout(formLayout)
        self.setLayout(self.layout)
        self.file_state=0
        self.timer = QtCore.QTimer()
        self.timermp1212 = QtCore.QTimer()
        self.popups = []
    
    def closeEvent(self, event):
        self.close
        super().closeEvent(event)
    
    def getfilebkg_file(self):
        self.filenamebkg = QFileDialog.getOpenFileName(self, 'Select the background image of same detector')
    
    def getfileblst_file(self):
        self.blacklist_file = QFileDialog.getOpenFileName(self, 'Select the list of peaks DAT file to blacklist')
    
    def predict_single_file(self,):
        ## Provide path to a single tiff or cor file to predict and write a pickle object
        filenameSingleExp = QFileDialog.getOpenFileName(self, 'Select a single experimental file')
        if len(filenameSingleExp[0]) == 0:
            return
        filenameSingleExp = filenameSingleExp[0]
        model_direc = self.modelDirec
        
        lim_x, lim_y = int(1), int(1)
                
        ## load model related files and generate the model
        if self.material_ != self.material1_:
            json_file = open(model_direc+"//model_"+self.material_+"_"+self.material1_+".json", 'r')
        else:
            json_file = open(model_direc+"//model_"+self.material_+".json", 'r')
                
        classhkl = np.load(model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
        angbins = np.load(model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
        
        if self.material_ != self.material1_:
            ind_mat = np.load(model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_5"]
            ind_mat1 = np.load(model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_6"]
        else: 
            ind_mat = None
            ind_mat1 = None  
        
        load_weights = self.filenameModel[0]
        wb = read_hdf5(load_weights)
        temp_key = list(wb.keys())
        
        # # load json and create model
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        print("Constructing model")
        load_weights = self.filenameModel[0]
        model.load_weights(load_weights)
        print("Uploading weights to model")
        print("All model files found and loaded")
        
        cond = self.strain_plot_tech.currentText()
        self.strain_calculation = False
        if cond == "YES":
            self.strain_calculation = True

        ## access grid files to process with multi-thread
        check = np.zeros(1)
        # =============================================================================
        try:
            blacklist = self.blacklist_file[0]
        except:
            blacklist = None
        
        ### Create a COR directory to be loaded in LaueTools
        cor_file_directory = self.filenameDirec + "//" + self.experimental_prefix.text()+"CORfiles"
        if not os.path.exists(cor_file_directory):
            os.makedirs(cor_file_directory)
        
        start_timemultiorimat = time.time()
        col = [[] for i in range(int(self.ubmat.text()))]
        colx = [[] for i in range(int(self.ubmat.text()))]
        coly = [[] for i in range(int(self.ubmat.text()))]
        rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
        match_rate = [[] for i in range(int(self.ubmat.text()))]
        spots_len = [[] for i in range(int(self.ubmat.text()))]
        iR_pix = [[] for i in range(int(self.ubmat.text()))]
        fR_pix = [[] for i in range(int(self.ubmat.text()))]
        mat_global = [[] for i in range(int(self.ubmat.text()))]
        best_match = [[] for i in range(int(self.ubmat.text()))]
        for i in range(int(self.ubmat.text())):
            col[i].append(np.zeros((lim_x*lim_y,3)))
            colx[i].append(np.zeros((lim_x*lim_y,3)))
            coly[i].append(np.zeros((lim_x*lim_y,3)))
            rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrixs[i].append(np.zeros((lim_x*lim_y,3,3)))
            match_rate[i].append(np.zeros((lim_x*lim_y,1)))
            spots_len[i].append(np.zeros((lim_x*lim_y,1)))
            iR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            fR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            mat_global[i].append(np.zeros((lim_x*lim_y,1)))
            best_match[i].append([[] for jk in range(lim_x*lim_y)])
            
        strain_matrix12multiorimat, strain_matrixs12multiorimat, \
        rotation_matrix12multiorimat, col12multiorimat, \
        colx12multiorimat, coly12multiorimat,\
        match_rate12multiorimat, mat_global12multiorimat, cnt12multiorimat,\
        files_treated12multiorimat, spots_len12multiorimat, \
        iR_pix12multiorimat, fR_pix12multiorimat, \
        check12multiorimat, best_match12multiorimat = predict_preprocessMP(filenameSingleExp, 0, 
                                                   rotation_matrix,strain_matrix,strain_matrixs,
                                                   col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                   mat_global,
                                                   check,self.detectorparameters,self.pixelsize,angbins,
                                                   classhkl, self.hkl_all_class0, self.hkl_all_class1, self.emin, self.emax,
                                                   self.material_, self.material1_, self.symmetry, self.symmetry1,lim_x,lim_y,
                                                   self.strain_calculation, ind_mat, ind_mat1,
                                                   model_direc, float(self.tolerance.text()), float(self.tolerance1.text()),
                                                   int(self.ubmat.text()), self.ccd_label.currentText(),
                                                   None,float(self.intensity_threshold.text()),
                                                   int(self.boxsize.text()),self.bkg_treatment.text(),
                                                   self.filenameDirec, self.experimental_prefix.text(),
                                                   blacklist, None, 
                                                   [],False,
                                                   wb, temp_key, cor_file_directory, "graphmode",
                                                    self.softmax_threshold_global,
                                                    self.mr_threshold_global,
                                                    self.cap_matchrate,
                                                    self.tolerance_strain,
                                                    self.tolerance_strain1,
                                                    self.NumberMaxofFits,
                                                    self.fit_peaks_gaussian_global,
                                                    self.FitPixelDev_global,
                                                    self.coeff,
                                                    self.coeff_overlap,
                                                    self.material0_limit,
                                                    self.material1_limit,
                                                    False,
                                                    self.material_phase_always_present,
                                                    self.crystal,
                                                    self.crystal1)
        end_timemultiorimat = time.time() - start_timemultiorimat
        print("Total time to process one file in graph mode (in seconds): "+str(end_timemultiorimat))        
        
        start_timebeamtime = time.time()
        col = [[] for i in range(int(self.ubmat.text()))]
        colx = [[] for i in range(int(self.ubmat.text()))]
        coly = [[] for i in range(int(self.ubmat.text()))]
        rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
        match_rate = [[] for i in range(int(self.ubmat.text()))]
        spots_len = [[] for i in range(int(self.ubmat.text()))]
        iR_pix = [[] for i in range(int(self.ubmat.text()))]
        fR_pix = [[] for i in range(int(self.ubmat.text()))]
        mat_global = [[] for i in range(int(self.ubmat.text()))]
        best_match = [[] for i in range(int(self.ubmat.text()))]
        for i in range(int(self.ubmat.text())):
            col[i].append(np.zeros((lim_x*lim_y,3)))
            colx[i].append(np.zeros((lim_x*lim_y,3)))
            coly[i].append(np.zeros((lim_x*lim_y,3)))
            rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrixs[i].append(np.zeros((lim_x*lim_y,3,3)))
            match_rate[i].append(np.zeros((lim_x*lim_y,1)))
            spots_len[i].append(np.zeros((lim_x*lim_y,1)))
            iR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            fR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            mat_global[i].append(np.zeros((lim_x*lim_y,1)))
            best_match[i].append([[] for jk in range(lim_x*lim_y)])
            
        strain_matrix12beamtime, strain_matrixs12beamtime, \
        rotation_matrix12beamtime, col12beamtime, \
        colx12beamtime, coly12beamtime,\
        match_rate12beamtime, mat_global12beamtime, cnt12beamtime,\
        files_treated12beamtime, spots_len12beamtime, \
        iR_pix12beamtime, fR_pix12beamtime, check12beamtime, \
        best_match12beamtime = predict_preprocessMP(filenameSingleExp, 0, 
                                                   rotation_matrix,strain_matrix,strain_matrixs,
                                                   col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                   mat_global,
                                                   check,self.detectorparameters,self.pixelsize,angbins,
                                                   classhkl, self.hkl_all_class0, self.hkl_all_class1, self.emin, self.emax,
                                                   self.material_, self.material1_, self.symmetry, self.symmetry1,lim_x,lim_y,
                                                   self.strain_calculation, ind_mat, ind_mat1,
                                                   model_direc, float(self.tolerance.text()), float(self.tolerance1.text()),
                                                   int(self.ubmat.text()), self.ccd_label.currentText(),
                                                   None,float(self.intensity_threshold.text()),
                                                   int(self.boxsize.text()),self.bkg_treatment.text(),
                                                   self.filenameDirec, self.experimental_prefix.text(),
                                                   blacklist, None, 
                                                   [],False,
                                                   wb, temp_key, cor_file_directory, "beamtime",
                                                    self.softmax_threshold_global,
                                                    self.mr_threshold_global,
                                                    self.cap_matchrate,
                                                    self.tolerance_strain,
                                                    self.tolerance_strain1,
                                                    self.NumberMaxofFits,
                                                    self.fit_peaks_gaussian_global,
                                                    self.FitPixelDev_global,
                                                    self.coeff,
                                                    self.coeff_overlap,
                                                    self.material0_limit,
                                                    self.material1_limit,
                                                    False,
                                                    self.material_phase_always_present,
                                                    self.crystal,
                                                    self.crystal1)
        end_timebeamtime = time.time() - start_timebeamtime
        print("Total time to process one file in beamtime mode (in seconds): "+str(end_timebeamtime))
        
        start_timefast = time.time()
        col = [[] for i in range(int(self.ubmat.text()))]
        colx = [[] for i in range(int(self.ubmat.text()))]
        coly = [[] for i in range(int(self.ubmat.text()))]
        rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
        match_rate = [[] for i in range(int(self.ubmat.text()))]
        spots_len = [[] for i in range(int(self.ubmat.text()))]
        iR_pix = [[] for i in range(int(self.ubmat.text()))]
        fR_pix = [[] for i in range(int(self.ubmat.text()))]
        mat_global = [[] for i in range(int(self.ubmat.text()))]
        best_match = [[] for i in range(int(self.ubmat.text()))]
        for i in range(int(self.ubmat.text())):
            col[i].append(np.zeros((lim_x*lim_y,3)))
            colx[i].append(np.zeros((lim_x*lim_y,3)))
            coly[i].append(np.zeros((lim_x*lim_y,3)))
            rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrixs[i].append(np.zeros((lim_x*lim_y,3,3)))
            match_rate[i].append(np.zeros((lim_x*lim_y,1)))
            spots_len[i].append(np.zeros((lim_x*lim_y,1)))
            iR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            fR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            mat_global[i].append(np.zeros((lim_x*lim_y,1)))
            best_match[i].append([[] for jk in range(lim_x*lim_y)])
            
        strain_matrix12fast, strain_matrixs12fast, \
        rotation_matrix12fast, col12fast, \
        colx12fast, coly12fast,\
        match_rate12fast, mat_global12fast, cnt12fast,\
        files_treated12fast, spots_len12fast, \
        iR_pix12fast, fR_pix12fast, check12fast, \
        best_match12fast = predict_preprocessMP(filenameSingleExp, 0, 
                                                   rotation_matrix,strain_matrix,strain_matrixs,
                                                   col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                   mat_global,
                                                   check,self.detectorparameters,self.pixelsize,angbins,
                                                   classhkl, self.hkl_all_class0, self.hkl_all_class1, self.emin, self.emax,
                                                   self.material_, self.material1_, self.symmetry, self.symmetry1,lim_x,lim_y,
                                                   self.strain_calculation, ind_mat, ind_mat1,
                                                   model_direc, float(self.tolerance.text()), float(self.tolerance1.text()),
                                                   int(self.ubmat.text()), self.ccd_label.currentText(),
                                                   None,float(self.intensity_threshold.text()),
                                                   int(self.boxsize.text()),self.bkg_treatment.text(),
                                                   self.filenameDirec, self.experimental_prefix.text(),
                                                   blacklist, None, 
                                                   [],False,
                                                   wb, temp_key, cor_file_directory, "fast",
                                                    self.softmax_threshold_global,
                                                    self.mr_threshold_global,
                                                    self.cap_matchrate,
                                                    self.tolerance_strain,
                                                    self.tolerance_strain1,
                                                    self.NumberMaxofFits,
                                                    self.fit_peaks_gaussian_global,
                                                    self.FitPixelDev_global,
                                                    self.coeff,
                                                    self.coeff_overlap,
                                                    self.material0_limit,
                                                    self.material1_limit,
                                                    False,
                                                    self.material_phase_always_present,
                                                    self.crystal,
                                                    self.crystal1)
        end_timefast = time.time() - start_timefast
        print("Total time to process one file in fast mode (in seconds): "+str(end_timefast)) 
        
        start_time = time.time()
        col = [[] for i in range(int(self.ubmat.text()))]
        colx = [[] for i in range(int(self.ubmat.text()))]
        coly = [[] for i in range(int(self.ubmat.text()))]
        rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrix = [[] for i in range(int(self.ubmat.text()))]
        strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
        match_rate = [[] for i in range(int(self.ubmat.text()))]
        spots_len = [[] for i in range(int(self.ubmat.text()))]
        iR_pix = [[] for i in range(int(self.ubmat.text()))]
        fR_pix = [[] for i in range(int(self.ubmat.text()))]
        mat_global = [[] for i in range(int(self.ubmat.text()))]
        best_match = [[] for i in range(int(self.ubmat.text()))]
        for i in range(int(self.ubmat.text())):
            col[i].append(np.zeros((lim_x*lim_y,3)))
            colx[i].append(np.zeros((lim_x*lim_y,3)))
            coly[i].append(np.zeros((lim_x*lim_y,3)))
            rotation_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrix[i].append(np.zeros((lim_x*lim_y,3,3)))
            strain_matrixs[i].append(np.zeros((lim_x*lim_y,3,3)))
            match_rate[i].append(np.zeros((lim_x*lim_y,1)))
            spots_len[i].append(np.zeros((lim_x*lim_y,1)))
            iR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            fR_pix[i].append(np.zeros((lim_x*lim_y,1)))
            mat_global[i].append(np.zeros((lim_x*lim_y,1)))
            best_match[i].append([[] for jk in range(lim_x*lim_y)])
            
        strain_matrix12, strain_matrixs12, \
        rotation_matrix12, col12, \
        colx12, coly12,\
        match_rate12, mat_global12, cnt12,\
        files_treated12, spots_len12, \
        iR_pix12, fR_pix12, check12, \
            best_match12 = predict_preprocessMP(filenameSingleExp, 0, 
                                                   rotation_matrix,strain_matrix,strain_matrixs,
                                                   col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                   mat_global,
                                                   check,self.detectorparameters,self.pixelsize,angbins,
                                                   classhkl, self.hkl_all_class0, self.hkl_all_class1, self.emin, self.emax,
                                                   self.material_, self.material1_, self.symmetry, self.symmetry1,lim_x,lim_y,
                                                   self.strain_calculation, ind_mat, ind_mat1,
                                                   model_direc, float(self.tolerance.text()), float(self.tolerance1.text()),
                                                   int(self.ubmat.text()), self.ccd_label.currentText(),
                                                   None,float(self.intensity_threshold.text()),
                                                   int(self.boxsize.text()),self.bkg_treatment.text(),
                                                   self.filenameDirec, self.experimental_prefix.text(),
                                                   blacklist, None, 
                                                   [],False,
                                                   wb, temp_key, cor_file_directory, "slow",
                                                    self.softmax_threshold_global,
                                                    self.mr_threshold_global,
                                                    self.cap_matchrate,
                                                    self.tolerance_strain,
                                                    self.tolerance_strain1,
                                                    self.NumberMaxofFits,
                                                    self.fit_peaks_gaussian_global,
                                                    self.FitPixelDev_global,
                                                    self.coeff,
                                                    self.coeff_overlap,
                                                    self.material0_limit,
                                                    self.material1_limit,
                                                    False,
                                                    self.material_phase_always_present,
                                                    self.crystal,
                                                    self.crystal1)
        end_time = time.time() - start_time
        print("Total time to process one file in slow mode (in seconds): "+str(end_time))
        
        save_name = filenameSingleExp.split(".")[0].split("/")[-1]
        np.savez_compressed(model_direc+'//'+save_name+'_SLOW_MODE.npz', strain_matrix12, strain_matrixs12, \
                                    rotation_matrix12, col12, \
                                        colx12, coly12,\
                                match_rate12, mat_global12, cnt12,\
                                    files_treated12, spots_len12, \
                                        iR_pix12, fR_pix12, check12, best_match12)
            
        w = MyPopup(match_rate12, rotation_matrix12, mat_global12, fR_pix12, 
                    filenameSingleExp, strain_matrix12, strain_matrixs12, end_time,
                    match_rate12fast, rotation_matrix12fast, mat_global12fast, fR_pix12fast, 
                    strain_matrix12fast, strain_matrixs12fast, end_timefast,
                    match_rate12beamtime, rotation_matrix12beamtime, mat_global12beamtime, fR_pix12beamtime, 
                    strain_matrix12beamtime, strain_matrixs12beamtime, end_timebeamtime,
                    match_rate12multiorimat, rotation_matrix12multiorimat, mat_global12multiorimat, fR_pix12multiorimat, 
                    strain_matrix12multiorimat, strain_matrixs12multiorimat, end_timemultiorimat)
        # w.setGeometry(QRect(100, 100, 400, 200))
        w.show()       
        self.popups.append(w)
                            
    def save_btn(self,):
        curr_time = time.time()
        now = datetime.datetime.fromtimestamp(curr_time)
        c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
        
        save_directory_ = self.model_direc+"//results_"+self.material_+"_"+c_time
        if not os.path.exists(save_directory_):
            os.makedirs(save_directory_)
        
        np.savez_compressed(save_directory_+ "//results.npz", 
                            self.best_match, self.mat_global, self.rotation_matrix, self.strain_matrix, 
                            self.strain_matrixs,
                            self.col, self.colx, self.coly, self.match_rate, self.files_treated,
                            self.lim_x, self.lim_y, self.spots_len, self.iR_pix, self.fR_pix,
                            self.material_, self.material1_)
        
        ## intermediate saving of pickle objects with results
        with open(save_directory_+ "//results.pickle", "wb") as output_file:
                cPickle.dump([self.best_match, self.mat_global, self.rotation_matrix, self.strain_matrix, 
                              self.strain_matrixs,
                              self.col, self.colx, self.coly, self.match_rate, self.files_treated,
                              self.lim_x, self.lim_y, self.spots_len, self.iR_pix, self.fR_pix,
                              self.material_, self.material1_, self.lattice_, self.lattice1_,
                              self.symmetry, self.symmetry1, self.crystal, self.crystal1], output_file)     

        try:
            ## Write global text file with all results
            if self.material_ != self.material1_:
                text_file = open(save_directory_+"//prediction_stats_"+self.material_+"_"+self.material1_+".txt", "w")
            else:
                text_file = open(save_directory_+"//prediction_stats_"+self.material_+".txt", "w")
    
            filenames = list(np.unique(self.files_treated))
            filenames.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
            
            for i in range(self.lim_x*self.lim_y):
                text_file.write("# ********** \n")
                text_file.write("# Filename: "+ filenames[i] + "\n")
                for j in range(len(self.best_match)):
                    stats_ = self.best_match[j][0][i]
                    dev_eps_sample = self.strain_matrixs[j][0][i,:,:]
                    dev_eps = self.strain_matrix[j][0][i,:,:]
                    initial_residue = self.iR_pix[j][0][i][0]
                    final_residue = self.fR_pix[j][0][i][0]
                    mat = int(self.mat_global[j][0][i][0])
                    if mat == 0:
                        case = "None"
                    elif mat == 1:
                        case = self.material_
                    elif mat == 2:
                        case = self.material1_
                    
                    text_file.write("# ********** UB MATRIX "+str(j+1)+" \n")
                    text_file.write("Spot_index for 2 HKL are "+ str(stats_[0])+" ; "+ str(stats_[1])+ "\n")
                    text_file.write("HKL1 "+str(stats_[2])+"; HKL2 "+str(stats_[3])+"\n")
                    text_file.write("Coords of HKL1 "+str(stats_[4])+\
                                    "; coords of HKL2 "+str(stats_[5])+"\n")
                    text_file.write("Distance between 2 spots is "+ str(stats_[6])+ "\n")
                    text_file.write("Distance between 2 spots in LUT is "+ str(stats_[7])+ "\n")
                    text_file.write("Accuracy of NN for 2 HKL is "+ str(stats_[8])+\
                                    "% ; "+str(stats_[9])+ "% \n")
                    string1 = "Matched, Expected, Matching rate(%) : " + \
                                str(stats_[10]) +", "+str(stats_[11]) +", "+str(stats_[12])+" \n"
                    text_file.write(string1)
                    text_file.write("Rotation matrix for 2 HKL (multiplied by symmetry) is \n")
                    temp_ = stats_[14].flatten()
                    string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                                "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                                    "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
                    text_file.write(string1)
                    
                    text_file.write("dev_eps_sample is \n")
                    temp_ = dev_eps_sample.flatten()
                    string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                                "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                                    "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
                    text_file.write(string1)
    
                    text_file.write("dev_eps is \n")
                    temp_ = dev_eps.flatten()
                    string1 = "[["+str(temp_[0])+","+str(temp_[1])+","+str(temp_[2])+"],"+  \
                                "["+str(temp_[3])+","+str(temp_[4])+","+str(temp_[5])+"],"+  \
                                    "["+str(temp_[6])+","+str(temp_[7])+","+str(temp_[8])+"]]"+ " \n"  
                    text_file.write(string1)
    
                    text_file.write("Initial_pixel, Final_pixel residues are : "+str(initial_residue)+", "+str(final_residue)+" \n")
                    
                    text_file.write("Mat_id is "+str(mat)+"\n")
                    text_file.write("Material indexed is "+case+"\n")
                    text_file.write("\n")
            text_file.close()
            print("prediction statistics are generated") 
        except:
            print("Errors with writing prediction output text file; could be the prediction was stopped midway")
        
        try:
            ## write MTEX file
            rotation_matrix = [[] for i in range(len(self.rotation_matrix))]
            for i in range(len(self.rotation_matrix)):
                rotation_matrix[i].append(np.zeros((self.lim_x*self.lim_y,3,3)))
    
            for i in range(len(self.rotation_matrix)):
                temp_mat = self.rotation_matrix[i][0]    
                for j in range(len(temp_mat)):
                    orientation_matrix = temp_mat[j,:,:]
                    ## rotate orientation by 40degrees to bring in Sample RF
                    omega = np.deg2rad(-40.0)
                    # # rotation de -omega autour de l'axe x (or Y?) pour repasser dans Rsample
                    cw = np.cos(omega)
                    sw = np.sin(omega)
                    mat_from_lab_to_sample_frame = np.array([[cw, 0.0, sw], [0.0, 1.0, 0.0], [-sw, 0, cw]]) #Y
                    # mat_from_lab_to_sample_frame = np.array([[1.0, 0.0, 0.0], [0.0, cw, -sw], [0.0, sw, cw]]) #X
                    # mat_from_lab_to_sample_frame = np.array([[cw, -sw, 0.0], [sw, cw, 0.0], [0.0, 0.0, 1.0]]) #Z
                    orientation_matrix = np.dot(mat_from_lab_to_sample_frame.T, orientation_matrix)
                    if np.linalg.det(orientation_matrix) < 0:
                        orientation_matrix = -orientation_matrix
                    rotation_matrix[i][0][j,:,:] = orientation_matrix
                              
            if self.material_ == self.material1_:
                lattice = self.lattice_
                material0_LG = material0_lauegroup
                header = [
                        "Channel Text File",
                        "Prj     lauetoolsnn",
                        "Author    [Ravi raj purohit]",
                        "JobMode    Grid",
                        "XCells    "+str(self.lim_x),
                        "YCells    "+str(self.lim_y),
                        "XStep    1.0",
                        "YStep    1.0",
                        "AcqE1    0",
                        "AcqE2    0",
                        "AcqE3    0",
                        "Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0",
                        "Phases    1",
                        str(lattice._lengths[0]*10)+";"+str(lattice._lengths[1]*10)+";"+\
                        str(lattice._lengths[2]*10)+"\t"+str(lattice._angles[0])+";"+\
                            str(lattice._angles[1])+";"+str(lattice._angles[2])+"\t"+"Material1"+ "\t"+material0_LG+ "\t"+"????"+"\t"+"????",
                        "Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS"]
            else:
                lattice = self.lattice_
                lattice1 = self.lattice1_
                material0_LG = material0_lauegroup
                material1_LG = material1_lauegroup
                header = [
                        "Channel Text File",
                        "Prj     lauetoolsnn",
                        "Author    [Ravi raj purohit]",
                        "JobMode    Grid",
                        "XCells    "+str(self.lim_x),
                        "YCells    "+str(self.lim_y),
                        "XStep    1.0",
                        "YStep    1.0",
                        "AcqE1    0",
                        "AcqE2    0",
                        "AcqE3    0",
                        "Euler angles refer to Sample Coordinate system (CS0)!    Mag    100    Coverage    100    Device    0    KV    15    TiltAngle    40    TiltAxis    0",
                        "Phases    2",
                        str(lattice._lengths[0]*10)+";"+str(lattice._lengths[1]*10)+";"+\
                        str(lattice._lengths[2]*10)+"\t"+str(lattice._angles[0])+";"+\
                            str(lattice._angles[1])+";"+str(lattice._angles[2])+"\t"+"Material1"+ "\t"+material0_LG+ "\t"+"????"+"\t"+"????",
                        str(lattice1._lengths[0]*10)+";"+str(lattice1._lengths[1]*10)+";"+\
                        str(lattice1._lengths[2]*10)+"\t"+str(lattice1._angles[0])+";"+\
                            str(lattice1._angles[1])+";"+str(lattice1._angles[2])+"\t"+"Material2"+ "\t"+material1_LG+ "\t"+"????"+"\t"+"????",
                        "Phase    X    Y    Bands    Error    Euler1    Euler2    Euler3    MAD    BC    BS"]
            # =================CALCULATION OF POSITION=====================================
            for index in range(len(self.rotation_matrix)):
                euler_angles = np.zeros((len(rotation_matrix[index][0]),3))
                phase_euler_angles = np.zeros(len(rotation_matrix[index][0]))
                for i in range(len(rotation_matrix[index][0])):
                    if np.all(rotation_matrix[index][0][i,:,:] == 0):
                        continue
                    euler_angles[i,:] = rot_mat_to_euler(rotation_matrix[index][0][i,:,:])
                    phase_euler_angles[i] = self.mat_global[index][0][i]        
                
                euler_angles = euler_angles.reshape((self.lim_x,self.lim_y,3))
                phase_euler_angles = phase_euler_angles.reshape((self.lim_x,self.lim_y,1))
                
                a = euler_angles
                if self.material_ != self.material1_:
                    filename125 = save_directory_+ "//"+self.material_+"_"+self.material1_+"_MTEX_UBmat_"+str(index)+".ctf"
                else:
                    filename125 = save_directory_+ "//"+self.material_+"_MTEX_UBmat_"+str(index)+".ctf"
                    
                f = open(filename125, "w")
                for ij in range(len(header)):
                    f.write(header[ij]+" \n")
                        
                for i123 in range(euler_angles.shape[1]):
                    y_step = 1 * i123
                    for j123 in range(euler_angles.shape[0]):
                        x_step = 1 * j123
                        phase_id = int(phase_euler_angles[j123,i123,0])
                        eul =  str(phase_id)+'\t' + "%0.4f" % x_step +'\t'+"%0.4f" % y_step+'\t8\t0\t'+ \
                                            "%0.4f" % a[j123,i123,0]+'\t'+"%0.4f" % a[j123,i123,1]+ \
                                                '\t'+"%0.4f" % a[j123,i123,2]+'\t0.0001\t180\t0\n'
                        string = eul
                        f.write(string)
                f.close()
        except:
            print("Error writing the MTEX file, could be the prediction data is not completed and save function was called")
         
        #%  Plot some data  
        try:
            global_plots(self.lim_x, self.lim_y, self.strain_matrix, self.strain_matrixs, self.col, 
                         self.colx, self.coly, self.match_rate, self.mat_global, self.spots_len, 
                         self.iR_pix, self.fR_pix, save_directory_, self.material_, self.material1_,
                         match_rate_threshold=5, bins=30)
        except:
            print("Error in the global plots module")
        
        try:
            save_sst(self.lim_x, self.lim_y, self.strain_matrix, self.strain_matrixs, self.col, 
                    self.colx, self.coly, self.match_rate, self.mat_global, self.spots_len, 
                    self.iR_pix, self.fR_pix, save_directory_, self.material_, self.material1_,
                    self.lattice_, self.lattice1_, self.symmetry, self.symmetry1, self.crystal, self.crystal1,
                    self.rotation_matrix, self.symmetry_name, self.symmetry1_name,
                          mac_axis = [0., 0., 1.], axis_text="Z", match_rate_threshold=5)
        except:
            print("Error in the SST plots module")
            
        ## HKL selective plots (in development)
        hkls_list = ast.literal_eval(self.hkl_plot.text())
        if self.ipf_axis.currentText() == "Z":
            mac_axis = [0., 0., 1.]
        elif self.ipf_axis.currentText() == "Y":
            mac_axis = [0., 1., 0.]
        elif self.ipf_axis.currentText() == "X":
            mac_axis = [1., 0., 0.]
        print(mac_axis, hkls_list)
        # save_hkl_stats(self.lim_x, self.lim_y, self.strain_matrix, self.strain_matrixs, self.col, 
        #               self.colx, self.coly, self.match_rate, self.mat_global, self.spots_len, 
        #               self.iR_pix, self.fR_pix, save_directory_, self.material_, self.material1_,
        #               self.lattice_, self.lattice1_, self.symmetry, self.symmetry1, self.rotation_matrix, 
        #              hkls_list=hkls_list, angle=10., mac_axis = mac_axis, axis_text = self.ipf_axis.currentText())
        
    def plot_pc(self):
        ## update matrix plot box?
        if self.cnt_matrix:
            self.cnt_matrix = False
            for intmat in range(int(self.ubmat.text())):
                if intmat == 0:
                    continue
                self.matrix_plot.addItem(str(intmat+1))
        
        self.btn_config.setEnabled(False)
        self.model_direc = self.modelDirec
        
        self.lim_x, self.lim_y = int(self.image_grid.text().split(",")[0]), int(self.image_grid.text().split(",")[1])
        
        if self.cnt == 0:
            self.col = [[] for i in range(int(self.ubmat.text()))]
            self.colx = [[] for i in range(int(self.ubmat.text()))]
            self.coly = [[] for i in range(int(self.ubmat.text()))]
            self.rotation_matrix = [[] for i in range(int(self.ubmat.text()))]
            self.strain_matrix = [[] for i in range(int(self.ubmat.text()))]
            self.strain_matrixs = [[] for i in range(int(self.ubmat.text()))]
            self.match_rate = [[] for i in range(int(self.ubmat.text()))]
            self.spots_len = [[] for i in range(int(self.ubmat.text()))]
            self.iR_pix = [[] for i in range(int(self.ubmat.text()))]
            self.fR_pix = [[] for i in range(int(self.ubmat.text()))]
            self.mat_global = [[] for i in range(int(self.ubmat.text()))]
            self.best_match = [[] for i in range(int(self.ubmat.text()))]
            for i in range(int(self.ubmat.text())):
                self.col[i].append(np.zeros((self.lim_x*self.lim_y,3)))
                self.colx[i].append(np.zeros((self.lim_x*self.lim_y,3)))
                self.coly[i].append(np.zeros((self.lim_x*self.lim_y,3)))
                self.rotation_matrix[i].append(np.zeros((self.lim_x*self.lim_y,3,3)))
                self.strain_matrix[i].append(np.zeros((self.lim_x*self.lim_y,3,3)))
                self.strain_matrixs[i].append(np.zeros((self.lim_x*self.lim_y,3,3)))
                self.match_rate[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.spots_len[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.iR_pix[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.fR_pix[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.mat_global[i].append(np.zeros((self.lim_x*self.lim_y,1)))
                self.best_match[i].append([[] for jk in range(self.lim_x*self.lim_y)])
                
        ## load model related files and generate the model
        if self.material_ != self.material1_:
            json_file = open(self.model_direc+"//model_"+self.material_+"_"+self.material1_+".json", 'r')
        else:
            json_file = open(self.model_direc+"//model_"+self.material_+".json", 'r')
                
        self.classhkl = np.load(self.model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_0"]
        self.angbins = np.load(self.model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_1"]
        
        if self.material_ != self.material1_:
            self.ind_mat = np.load(self.model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_5"]
            self.ind_mat1 = np.load(self.model_direc+"//MOD_grain_classhkl_angbin.npz")["arr_6"]
        else: 
            self.ind_mat = None
            self.ind_mat1 = None  
        
        load_weights = self.filenameModel[0]
        self.wb = read_hdf5(load_weights)
        self.temp_key = list(self.wb.keys())
        
        # # load json and create model
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = model_from_json(loaded_model_json)
        print("Constructing model")
        load_weights = self.filenameModel[0]
        self.model.load_weights(load_weights)
        print("Uploading weights to model")
        print("All model files found and loaded")

        if self.file_state==0:
            ct = time.time()
            now = datetime.datetime.fromtimestamp(ct)
            self.c_time = now.strftime("%Y-%m-%d_%H-%M-%S")
            self.file_state = 1
        
        self.update_plot()
        
        self.timer.setInterval(500) ## check every second (update the list of files in folder)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        
        self.mode_spotCycle = self.analysis_plot_tech.currentText()
        
        if self.matrix_plot_tech.currentText() == "MultiProcessing":
            self.ncpu = cpu_count_user
            self._inputs_queue = Queue()
            self._outputs_queue = Queue()
            #TODO
            ## create a shared rotation matrix to be used by all process
            #if self.use_previous_UBmatrix_name:
            #    mp_rotation_matrix = multip.Array(c_type.c_double, int(self.ubmat.text())*self.lim_x*self.lim_y*3*3)
            #else:
            #    mp_rotation_matrix = None
            run_flag = multip.Value('I', True)
            self._worker_processes = {}
            for i in range(self.ncpu):
                self._worker_processes[i]= Process(target=AnotherWindowLivePrediction.worker, args=(self._inputs_queue, self._outputs_queue, i+1, run_flag))#, mp_rotation_matrix))
            for i in range(self.ncpu):
                self._worker_processes[i].start()
            ### Update data from multiprocessing
            self.timermp1212.setInterval(100) ## check every second (update the list of files in folder)
            self.timermp1212.timeout.connect(self.update_data_mp1212)
            self.timermp1212.start()
    
        self.out_name = None
        self.run = True
        self.temp_ = threading.Thread(target=self.plot_pcv1, daemon=False)
        self.temp_.start()
        self.btn_stop.setEnabled(True)
        self.btn_save.setEnabled(False)
                                
    def update_plot(self):
        ## get color matrix to plot
        index_plotfnc = int(self.matrix_plot.currentText())-1
        strain_index_plotfnc = self.strain_plot.currentText()
        
        if "sample" in strain_index_plotfnc:
            title_plotfnc = "Deviatoric strain (sample frame)"
            strain_matrix_plot_plotfnc = self.strain_matrixs[index_plotfnc][0]
        elif "crystal" in strain_index_plotfnc:
            title_plotfnc = "Deviatoric strain (crystal frame)"
            strain_matrix_plot_plotfnc = self.strain_matrix[index_plotfnc][0]
        
        if "11" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,0,0]
        elif "22" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,1,1]
        elif "33" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,2,2]
        elif "12" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,0,1]
        elif "13" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,0,2]
        elif "23" in strain_index_plotfnc:
            strain_matrix_plot_plotfnc = strain_matrix_plot_plotfnc[:,1,2]
        
        try:
            strain_tensor_plot_plotfnc = strain_matrix_plot_plotfnc.reshape((self.lim_x, self.lim_y))
        except:
            print("Reshape error, verify the grid xlim and ylim and change them")
            return
        
        if self.ipf_axis.currentText() == "Z":
            col_plot_plotfnc = self.col[index_plotfnc][0]
        elif self.ipf_axis.currentText() == "Y":
            col_plot_plotfnc = self.coly[index_plotfnc][0]
        elif self.ipf_axis.currentText() == "X":
            col_plot_plotfnc = self.colx[index_plotfnc][0]

        col_plot_plotfnc = col_plot_plotfnc.reshape((self.lim_x, self.lim_y, 3))
        mr_plot_plotfnc = self.match_rate[index_plotfnc][0]
        mr_plot_plotfnc = mr_plot_plotfnc.reshape((self.lim_x, self.lim_y))        
        mat_glob_plotfnc = self.mat_global[index_plotfnc][0]
        mat_glob_plotfnc = mat_glob_plotfnc.reshape((self.lim_x, self.lim_y))
        
        # Drop off the first y element, append a new one.
        self.canvas.axes.cla()
        self.canvas.axes.set_title("IPF map", loc='center', fontsize=8)
        self.canvas.axes.imshow(col_plot_plotfnc, origin='lower')
        self.canvas.axes2.cla()
        self.canvas.axes2.set_title(title_plotfnc, loc='center', fontsize=8) 
        self.canvas.axes2.imshow(strain_tensor_plot_plotfnc, origin='lower')
        self.canvas.axes1.cla()
        self.canvas.axes1.set_title("Matching rate", loc='center', fontsize=8) 
        self.canvas.axes1.imshow(mr_plot_plotfnc, origin='lower')
        
        if self.material_ != self.material1_:
            self.canvas.axes3.cla()
            self.canvas.axes3.set_title("Material Index (1: "+self.material_+"; 2: "+self.material1_+")", loc='center', fontsize=8) 
            self.canvas.axes3.imshow(mat_glob_plotfnc, origin='lower')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
    
    def onclickImage(self, event123):
        ix, iy = event123.xdata, event123.ydata
        try:
            ## read the saved COR file and extract exp spots info.## avoid zero index problem
            ix = int(round(ix))
            iy = int(round(iy))
            try:
                # self.lim_x * self.lim_y
                if iy == 0 and ix == 0:
                    image_no = 0
                elif iy == 0 and ix != 0:
                    image_no = ix
                elif iy != 0 and ix == 0:
                    image_no = iy * self.lim_y
                elif iy != 0 and ix != 0:
                    image_no = iy * self.lim_y + ix
                    
                # image_no = int(ix*iy+(iy-1)-1)
                index_plotfnc = int(self.matrix_plot.currentText())-1
                rotation_matrix = self.rotation_matrix[index_plotfnc][0][image_no,:,:]
                mat_glob_plotfnc = self.mat_global[index_plotfnc][0][image_no]
                path = os.path.normpath(self.filenm[image_no].decode())
                files = self.cor_file_directory+"//"+path.split(os.sep)[-1].split(".")[0]+".cor"        
                allres = IOLT.readfile_cor(files, True)
                data_theta, data_chi, peakx, peaky, intensity = allres[1:6]
                CCDcalib = allres[-1]
                detectorparameters = allres[-2]
                # print('detectorparameters from file are: '+ str(detectorparameters))
                pixelsize = CCDcalib['pixelsize']
                CCDLabel = CCDcalib['CCDLabel']
                framedim = dictLT.dict_CCD[CCDLabel][0]
                dict_dp={}
                dict_dp['kf_direction']='Z>0'
                dict_dp['detectorparameters']=detectorparameters
                dict_dp['detectordistance']=detectorparameters[0]
                dict_dp['detectordiameter']=pixelsize*framedim[0]
                dict_dp['pixelsize']=pixelsize
                dict_dp['dim']=framedim
                dict_dp['peakX']=peakx
                dict_dp['peakY']=peaky
                dict_dp['intensity']=intensity
            except:
                print("No COR file could be found for the selected pixel")
                return
                    
            if mat_glob_plotfnc == 1:
                material_=self.material_
                tolerance_add = float(self.tolerance.text())                
            elif mat_glob_plotfnc == 2:
                material_=self.material1_
                tolerance_add = float(self.tolerance1.text())
            else:
                print("No Material is indexed for this pixel")
                material_ = None
                tolerance_add = None
                sim_twotheta = []
                sim_chi = []
                list_spots = []
                residues = []
                theo_index = []
            
            if np.all(rotation_matrix==0):
                material_ = None
                sim_twotheta = []
                sim_chi = []
                list_spots = []
                residues = []
                theo_index = []
                print("No rotation matrix found")
            
            if material_ != None:
                sim_twotheta, sim_chi, list_spots, residues, theo_index = simulate_spots(rotation_matrix, 
                                                                            material_, self.emax, self.emin, 
                                                                            dict_dp['detectorparameters'], dict_dp,
                                                                            tolerance_add, data_theta*2.0,
                                                                            data_chi)
                if len(sim_twotheta) == 0:
                    sim_twotheta = []
                    sim_chi = []
                    list_spots = []
                    residues = []
                    theo_index = []
                    print("Nothing simulated")
            
            w = MyPopup_image(data_theta, data_chi, intensity, sim_twotheta, sim_chi, ix, iy, files,
                              list_spots, residues, theo_index)
            w.show()       
            self.popups.append(w)
            print('chosen pixel coords are x = %d, y = %d'%(ix, iy))
        except:
            print("Error occured")
        
    def update_data_mp1212(self):
        if not self._outputs_queue.empty():            
            self.timermp1212.blockSignals(True)         
            n_range = self._outputs_queue.qsize()
            for _ in range(n_range):
                r_message_mpdata = self._outputs_queue.get()
                strain_matrix_mpdata, strain_matrixs_mpdata, rotation_matrix_mpdata, col_mpdata, \
                                 colx_mpdata, coly_mpdata, match_rate_mpdata, mat_global_mpdata, \
                                     cnt_mpdata, meta_mpdata, files_treated_mpdata, spots_len_mpdata, \
                                         iR_pixel_mpdata, fR_pixel_mpdata, best_match_mpdata, check_mpdata = r_message_mpdata
    
                for i_mpdata in files_treated_mpdata:
                    self.files_treated.append(i_mpdata)
                    
                self.check[cnt_mpdata] = check_mpdata[cnt_mpdata]
                for intmat_mpdata in range(int(self.ubmat.text())):
                    self.mat_global[intmat_mpdata][0][cnt_mpdata] = mat_global_mpdata[intmat_mpdata][0][cnt_mpdata]
                    self.strain_matrix[intmat_mpdata][0][cnt_mpdata,:,:] = strain_matrix_mpdata[intmat_mpdata][0][cnt_mpdata,:,:]
                    self.strain_matrixs[intmat_mpdata][0][cnt_mpdata,:,:] = strain_matrixs_mpdata[intmat_mpdata][0][cnt_mpdata,:,:]
                    self.rotation_matrix[intmat_mpdata][0][cnt_mpdata,:,:] = rotation_matrix_mpdata[intmat_mpdata][0][cnt_mpdata,:,:]
                    self.col[intmat_mpdata][0][cnt_mpdata,:] = col_mpdata[intmat_mpdata][0][cnt_mpdata,:]
                    self.colx[intmat_mpdata][0][cnt_mpdata,:] = colx_mpdata[intmat_mpdata][0][cnt_mpdata,:]
                    self.coly[intmat_mpdata][0][cnt_mpdata,:] = coly_mpdata[intmat_mpdata][0][cnt_mpdata,:]
                    self.match_rate[intmat_mpdata][0][cnt_mpdata] = match_rate_mpdata[intmat_mpdata][0][cnt_mpdata]
                    self.spots_len[intmat_mpdata][0][cnt_mpdata] = spots_len_mpdata[intmat_mpdata][0][cnt_mpdata]
                    self.iR_pix[intmat_mpdata][0][cnt_mpdata] = iR_pixel_mpdata[intmat_mpdata][0][cnt_mpdata]
                    self.fR_pix[intmat_mpdata][0][cnt_mpdata] = fR_pixel_mpdata[intmat_mpdata][0][cnt_mpdata]
                    self.best_match[intmat_mpdata][0][cnt_mpdata] = best_match_mpdata[intmat_mpdata][0][cnt_mpdata] 
                try:
                #TODO
                #Perhaps save only the best matching rate UB matricies in the file, instead of all UB matricies
                #Or select only the best UB matricies when opening the file in propose_UBmatrix function
                    ## calculate average matching rate and save it
                    avg_match_rate1 = [[] for i in range(int(self.ubmat.text()))]
                    for intmat_mpdata in range(int(self.ubmat.text())):
                        avg_match_rate = []
                        for j in self.match_rate[intmat_mpdata][0][:]:
                            if j != 0:
                                avg_match_rate.append(j)
                        avg_match_rate1[intmat_mpdata].append(np.median(avg_match_rate))
                    np.savez_compressed(self.model_direc+'//rotation_matrix_indexed.npz', 
                                        self.rotation_matrix, self.mat_global, 
                                        self.match_rate, avg_match_rate1)
                except:
                    print("Warning : Error saving the NPZ file; nothing to worry")
            self.timermp1212.blockSignals(False)
    
    @staticmethod
    def worker(inputs_queue, outputs_queue, proc_id, run_flag):#, mp_rotation_matrix):
        print(f'Initializing worker {proc_id}')
        while True:
            if not run_flag.value:
                break
            time.sleep(0.01)
            if not inputs_queue.empty(): 
                message = inputs_queue.get()
                if message == 'STOP':
                    print(f'[{proc_id}] stopping')
                    break

                num1, num2, meta = message
                files_worked = []
                while True:
                    if len(num1) == len(files_worked) or len(num1) == 0:
                        print("process finished")
                        break
                    for ijk in range(len(num1)):
                        if ijk in files_worked:
                            continue                       
                        if not run_flag.value:
                            num1, files_worked = [], []
                            print(f'[{proc_id}] stopping')
                            break
                        
                        files, cnt, rotation_matrix, strain_matrix, strain_matrixs,\
                        col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,mat_global,\
                        check,detectorparameters,pixelsize,angbins,\
                        classhkl, hkl_all_class0, hkl_all_class1, emin, emax,\
                        material_, material1_, symmetry, symmetry1,lim_x,lim_y,\
                        strain_calculation, ind_mat, ind_mat1,\
                        model_direc, tolerance , tolerance1,\
                        matricies, ccd_label,\
                        filename_bkg,intensity_threshold,\
                        boxsize,bkg_treatment,\
                        filenameDirec, experimental_prefix,\
                        blacklist_file, text_file, \
                        files_treated,try_previous1,\
                        wb, temp_key, cor_file_directory, mode_spotCycle1,\
                        softmax_threshold_global123,mr_threshold_global123,\
                        cap_matchrate123, tolerance_strain123, tolerance_strain1231,\
                        NumberMaxofFits123,fit_peaks_gaussian_global123,\
                        FitPixelDev_global123,coeff123,coeff_overlap,\
                        material0_limit, material1_limit, use_previous_UBmatrix_name1,\
                            material_phase_always_present1, crystal, crystal1 = num1[ijk]

                        if os.path.isfile(files):
                            # try:
                            strain_matrix12, strain_matrixs12, \
                                rotation_matrix12, col12, \
                                    colx12, coly12,\
                            match_rate12, mat_global12, cnt12,\
                                files_treated12, spots_len12, \
                                    iR_pix12, fR_pix12, check12, best_match12 = predict_preprocessMP(files, cnt, 
                                                                       rotation_matrix,strain_matrix,strain_matrixs,
                                                                       col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,
                                                                       mat_global,
                                                                       check,detectorparameters,pixelsize,angbins,
                                                                       classhkl, hkl_all_class0, hkl_all_class1, emin, emax,
                                                                       material_, material1_, symmetry, symmetry1,lim_x,lim_y,
                                                                       strain_calculation, ind_mat, ind_mat1,
                                                                       model_direc, tolerance, tolerance1,
                                                                       matricies, ccd_label,
                                                                       filename_bkg,intensity_threshold,
                                                                       boxsize,bkg_treatment,
                                                                       filenameDirec, experimental_prefix,
                                                                       blacklist_file, text_file, 
                                                                       files_treated,try_previous1,
                                                                       wb, temp_key, cor_file_directory, mode_spotCycle1,
                                                                       softmax_threshold_global123,mr_threshold_global123,
                                                                       cap_matchrate123, tolerance_strain123,
                                                                       tolerance_strain1231,NumberMaxofFits123,
                                                                       fit_peaks_gaussian_global123,
                                                                       FitPixelDev_global123, coeff123,coeff_overlap,
                                                                       material0_limit,material1_limit,
                                                                       use_previous_UBmatrix_name1,
                                                                       material_phase_always_present1,
                                                                       crystal, crystal1)#, mp_rotation_matrix)
                            if check12[cnt] == 1:
                                files_worked.append(ijk)
                                meta['proc_id'] = proc_id
                                r_message = (strain_matrix12, strain_matrixs12, rotation_matrix12, col12, \
                                             colx12, coly12, match_rate12, mat_global12, cnt12, meta, \
                                             files_treated12, spots_len12, iR_pix12, fR_pix12, best_match12, check12)
                                outputs_queue.put(r_message)
                            # except Exception as e:
                            #     print(e)
                            #     continue
        print("broke the worker while loop")
    
    def plot_pcv1(self):
        np.savez_compressed(self.model_direc+'//rotation_matrix_indexed.npz', self.rotation_matrix, self.mat_global, self.match_rate, 0.0)
        
        cond = self.strain_plot_tech.currentText()
        self.strain_calculation = False
        if cond == "YES":
            self.strain_calculation = True
            
        cond_mode = self.matrix_plot_tech.currentText()
        # =============================================================================
        #         ## Multi-processing routine
        # =============================================================================
        ## Number of files to generate
        grid_files = np.zeros((self.lim_x,self.lim_y))
        self.filenm = np.chararray((self.lim_x,self.lim_y), itemsize=1000)
        grid_files = grid_files.ravel()
        self.filenm = self.filenm.ravel()
        count_global = self.lim_x * self.lim_y
        
        if self.ccd_label.currentText() == "Cor" or self.ccd_label.currentText() == "cor":
            format_file = "cor"
        else:
            format_file = dictLT.dict_CCD[self.ccd_label.currentText()][7]

        list_of_files = glob.glob(self.filenameDirec+'//'+self.experimental_prefix.text()+'*.'+format_file)
        ## sort files
        ## TypeError: '<' not supported between instances of 'str' and 'int'
        list_of_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])

        if len(list_of_files) == count_global:
            for ii in range(len(list_of_files)):
                grid_files[ii] = ii
                self.filenm[ii] = list_of_files[ii]               
        else:
            print("expected "+str(count_global)+" files based on the XY grid ("+str(self.lim_x)+","+str(self.lim_y)+") defined by user")
            print("But found "+str(len(list_of_files))+" files (either all data is not written yet or maybe XY grid definition is not proper)")
            digits = len(str(count_global))
            digits = max(digits,4)

            for ii in range(count_global):
                text = str(ii)
                string = text.zfill(digits)
                file_name_temp = self.filenameDirec+'//'+self.experimental_prefix.text()+string+'.'+format_file
                ## store it in a grid 
                self.filenm[ii] = file_name_temp
            ## access grid files to process with multi-thread
        self.check = np.zeros(count_global)
        # =============================================================================
        try:
            blacklist = self.blacklist_file[0]
        except:
            blacklist = None
        
        ### Create a COR directory to be loaded in LaueTools
        self.cor_file_directory = self.filenameDirec + "//" + self.experimental_prefix.text()+"CORfiles"
        if not os.path.exists(self.cor_file_directory):
            os.makedirs(self.cor_file_directory)
        
        while True:
            if cond_mode == "Sequential":
                self.predict_preprocess(cnt=self.cnt, 
                                          rotation_matrix=self.rotation_matrix,
                                          strain_matrix=self.strain_matrix,
                                          strain_matrixs=self.strain_matrixs,
                                          col=self.col,
                                          colx=self.colx,
                                          coly=self.coly,
                                          match_rate=self.match_rate,
                                          spots_len=self.spots_len, 
                                          iR_pix=self.iR_pix, 
                                          fR_pix=self.fR_pix,
                                          best_match = self.best_match,
                                          mat_global=self.mat_global,
                                          check=self.check,
                                          detectorparameters=self.detectorparameters,
                                          pixelsize=self.pixelsize,
                                          angbins=self.angbins,
                                          classhkl=self.classhkl,
                                          hkl_all_class0=self.hkl_all_class0,
                                          hkl_all_class1=self.hkl_all_class1,
                                          emin=self.emin,
                                          emax=self.emax,
                                          material_=self.material_,
                                          material1_=self.material1_,
                                          symmetry=self.symmetry,
                                          symmetry1=self.symmetry1,   
                                          lim_x= self.lim_x,
                                          lim_y=self.lim_y,
                                          strain_calculation=self.strain_calculation, 
                                          ind_mat=self.ind_mat, ind_mat1=self.ind_mat1,
                                          model_direc=self.model_direc, tolerance=float(self.tolerance.text()),
                                          tolerance1=float(self.tolerance1.text()),
                                          matricies=int(self.ubmat.text()), ccd_label=self.ccd_label.currentText(), 
                                          filename_bkg=None, #self.filenamebkg,
                                          intensity_threshold=float(self.intensity_threshold.text()),
                                          boxsize=int(self.boxsize.text()),bkg_treatment=self.bkg_treatment.text(),
                                          filenameDirec=self.filenameDirec, 
                                          experimental_prefix=self.experimental_prefix.text(),
                                          blacklist_file =blacklist,
                                          text_file=None,
                                          files_treated=self.files_treated,
                                          try_previous1=True,
                                          wb = self.wb,
                                          temp_key = self.temp_key,
                                          cor_file_directory=self.cor_file_directory,
                                          mode_spotCycle1 = self.mode_spotCycle,
                                          softmax_threshold_global123 = self.softmax_threshold_global,
                                          mr_threshold_global123=self.mr_threshold_global,
                                          cap_matchrate123=self.cap_matchrate,
                                          tolerance_strain123=self.tolerance_strain,
                                          tolerance_strain1231=self.tolerance_strain1,
                                          NumberMaxofFits123=self.NumberMaxofFits,
                                          fit_peaks_gaussian_global123=self.fit_peaks_gaussian_global,
                                          FitPixelDev_global123=self.FitPixelDev_global,
                                          coeff123 = self.coeff,
                                          coeff_overlap=self.coeff_overlap,
                                          material0_limit=self.material0_limit,
                                          material1_limit=self.material1_limit,
                                          use_previous_UBmatrix_name=self.use_previous_UBmatrix_name,
                                          material_phase_always_present = self.material_phase_always_present,
                                          crystal=self.crystal,
                                          crystal1=self.crystal1)         
            elif cond_mode == "MultiProcessing":
                try_prevs = False
                if self.mode_spotCycle == "beamtime":
                    try_prevs = True
                
                valu12 = [[self.filenm[ii].decode(), ii,
                           self.rotation_matrix,
                            self.strain_matrix,
                            self.strain_matrixs,
                            self.col,
                            self.colx,
                            self.coly,
                            self.match_rate,
                            self.spots_len, 
                            self.iR_pix, 
                            self.fR_pix,
                            self.best_match,
                            self.mat_global,
                            self.check,
                            self.detectorparameters,
                            self.pixelsize,
                            self.angbins,
                            self.classhkl,
                            self.hkl_all_class0,
                            self.hkl_all_class1,
                            self.emin,
                            self.emax,
                            self.material_,
                            self.material1_,
                            self.symmetry,
                            self.symmetry1,   
                            self.lim_x,
                            self.lim_y,
                            self.strain_calculation, 
                            self.ind_mat, self.ind_mat1,
                            self.model_direc, float(self.tolerance.text()),
                            float(self.tolerance1.text()),
                            int(self.ubmat.text()), self.ccd_label.currentText(), 
                            None,
                            float(self.intensity_threshold.text()),
                            int(self.boxsize.text()),self.bkg_treatment.text(),
                            self.filenameDirec, 
                            self.experimental_prefix.text(),
                            blacklist,
                            None,
                            self.files_treated,
                            try_prevs, ## try previous is kept true, incase if its stuck in loop
                            self.wb,
                            self.temp_key,
                            self.cor_file_directory,
                            self.mode_spotCycle,
                            self.softmax_threshold_global,
                            self.mr_threshold_global,
                            self.cap_matchrate,
                            self.tolerance_strain,
                            self.tolerance_strain1,
                            self.NumberMaxofFits,
                            self.fit_peaks_gaussian_global,
                            self.FitPixelDev_global,
                            self.coeff,
                            self.coeff_overlap,
                            self.material0_limit,
                            self.material1_limit,
                            self.use_previous_UBmatrix_name,
                            self.material_phase_always_present,
                            self.crystal,
                            self.crystal1] for ii in range(count_global)]
                
                chunks = chunker_list(valu12, self.ncpu)
                chunks_mp = list(chunks)

                meta = {'t1':time.time()}
                for ijk in range(int(self.ncpu)):
                    self._inputs_queue.put((chunks_mp[ijk], self.ncpu, meta))
                    
            if cond_mode == "MultiProcessing":
                print("Launched all processes")
                break
            
            if (not self.run) or (self.cnt >= self.lim_x*self.lim_y):
                self.update_plot()
                print("BROKE the WHILE loop FREE")
                break

    def plot_btn_stop(self):
        self.timermp1212.blockSignals(False)
        if self.matrix_plot_tech.currentText() == "MultiProcessing":
            run_flag = multip.Value('I', False)
            while not self._outputs_queue.empty():            
                n_range = self._outputs_queue.qsize()
                for _ in range(n_range):
                    continue  
            print("Flag for mp module: ",run_flag)
            time.sleep(0.1)

        self.cnt = 1
        self.run = False
        self.timer.stop()
        self.timermp1212.stop()    
        
        self.btn_config.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.btn_save.setEnabled(True)
        
    def getfiles(self):
        self.modelDirec = QFileDialog.getExistingDirectory(self, 'Select Folder in which model files are located')
    
    def getfiles1(self):
        self.filenameDirec = QFileDialog.getExistingDirectory(self, 'Select Folder in which Experimental data is or will be stored')
    
    def getfileModel(self):
        self.filenameModel = QFileDialog.getOpenFileName(self, 'Select the model weights H5 or HDF5 file')
    
    def predict_preprocess(self,cnt,rotation_matrix,strain_matrix,strain_matrixs,
                            col,colx,coly,match_rate,spots_len,iR_pix,fR_pix,best_match,mat_global,
                            check,detectorparameters,pixelsize,angbins,
                            classhkl, hkl_all_class0, hkl_all_class1, emin, emax,
                            material_, material1_, symmetry, symmetry1,lim_x,lim_y,
                            strain_calculation, ind_mat, ind_mat1,
                            model_direc=None, tolerance =None, tolerance1 =None,
                           matricies=None, ccd_label=None,
                           filename_bkg=None,intensity_threshold=None,
                           boxsize=None,bkg_treatment=None,
                           filenameDirec=None, experimental_prefix=None,
                           blacklist_file =None, text_file=None, files_treated=None,try_previous1=False,
                           wb=None, temp_key=None, cor_file_directory=None, mode_spotCycle1=None,
                           softmax_threshold_global123=None,mr_threshold_global123=None,cap_matchrate123=None,
                           tolerance_strain123=None,tolerance_strain1231=None,NumberMaxofFits123=None,fit_peaks_gaussian_global123=None,
                           FitPixelDev_global123=None, coeff123=None,coeff_overlap=None,
                           material0_limit=None, material1_limit=None, use_previous_UBmatrix_name=None,
                           material_phase_always_present=None, crystal=None, crystal1=None):
        
        if ccd_label in ["Cor", "cor"]:
            format_file = "cor"
        else:
            format_file = dictLT.dict_CCD[ccd_label][7]

        list_of_files = glob.glob(filenameDirec+'//'+experimental_prefix+'*.'+format_file)
        ## sort files
        ## TypeError: '<' not supported between instances of 'str' and 'int'
        list_of_files.sort(key=lambda var:[int(x) if x.isdigit() else x for x in re.findall(r'[^0-9]|[0-9]+', var)])
        
        for files in list_of_files:
            peak_detection_error = False
            if self.run == False:
                break

            if files in files_treated:
                continue
            
            files_treated.append(files)
                        
            if files.split(".")[1] != "cor":
                CCDLabel=ccd_label
                seednumber = "Experimental "+CCDLabel+" file"    
                
                try:
                    out_name = blacklist_file
                except:
                    out_name = None  
                    
                if bkg_treatment == None:
                    bkg_treatment = "A-B"
                    
                try:
                    ### Max space = space betzeen pixles
                    peak_XY = RMCCD.PeakSearch(
                                                files,
                                                stackimageindex = -1,
                                                CCDLabel=CCDLabel,
                                                NumberMaxofFits=NumberMaxofFits123,
                                                PixelNearRadius=10,
                                                removeedge=2,
                                                IntensityThreshold=intensity_threshold,
                                                local_maxima_search_method=0,
                                                boxsize=boxsize,
                                                position_definition=1,
                                                verbose=0,
                                                fit_peaks_gaussian=fit_peaks_gaussian_global123,
                                                xtol=0.001,                
                                                FitPixelDev=FitPixelDev_global123,
                                                return_histo=0,
                                                # Saturation_value=1e10,  # to be merged in CCDLabel
                                                # Saturation_value_flatpeak=1e10,
                                                MinIntensity=0,
                                                PeakSizeRange=(0.65,200),
                                                write_execution_time=1,
                                                Data_for_localMaxima = "auto_background",
                                                formulaexpression=bkg_treatment,
                                                Remove_BlackListedPeaks_fromfile=out_name,
                                                reject_negative_baseline=True,
                                                Fit_with_Data_for_localMaxima=False,
                                                maxPixelDistanceRejection=15.0,
                                                )
                    peak_XY = peak_XY[0]#[:,:2] ##[2] Integer peak lists
                except:
                    print("Error in Peak detection for "+ files)
                    for intmat in range(matricies):
                        rotation_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                        strain_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                        strain_matrixs[intmat][0][cnt,:,:] = np.zeros((3,3))
                        col[intmat][0][cnt,:] = 0,0,0
                        colx[intmat][0][cnt,:] = 0,0,0
                        coly[intmat][0][cnt,:] = 0,0,0
                        match_rate[intmat][0][cnt] = 0
                        mat_global[intmat][0][cnt] = 0
                    
                    cnt += 1
                    peak_detection_error = True
                    continue
                
                s_ix = np.argsort(peak_XY[:, 2])[::-1]
                peak_XY = peak_XY[s_ix]
                
                framedim = dictLT.dict_CCD[CCDLabel][0]
                twicetheta, chi = Lgeo.calc_uflab(peak_XY[:,0], peak_XY[:,1], detectorparameters,
                                                    returnAngles=1,
                                                    pixelsize=pixelsize,
                                                    kf_direction='Z>0')
                data_theta, data_chi = twicetheta/2., chi
                
                framedim = dictLT.dict_CCD[CCDLabel][0]
                dict_dp={}
                dict_dp['kf_direction']='Z>0'
                dict_dp['detectorparameters']=detectorparameters
                dict_dp['detectordistance']=detectorparameters[0]
                dict_dp['detectordiameter']=pixelsize*framedim[0]
                dict_dp['pixelsize']=pixelsize
                dict_dp['dim']=framedim
                dict_dp['peakX']=peak_XY[:,0]
                dict_dp['peakY']=peak_XY[:,1]
                dict_dp['intensity']=peak_XY[:,2]
                
                CCDcalib = {"CCDLabel":CCDLabel,
                            "dd":detectorparameters[0], 
                            "xcen":detectorparameters[1], 
                            "ycen":detectorparameters[2], 
                            "xbet":detectorparameters[3], 
                            "xgam":detectorparameters[4],
                            "pixelsize": pixelsize}
                
                path = os.path.normpath(files)
                IOLT.writefile_cor(cor_file_directory+"//"+path.split(os.sep)[-1].split(".")[0], twicetheta, 
                                   chi, peak_XY[:,0], peak_XY[:,1], peak_XY[:,2],
                                   param=CCDcalib, sortedexit=0)
                
            elif files.split(".")[1] == "cor":
                seednumber = "Experimental COR file"
                allres = IOLT.readfile_cor(files, True)
                data_theta, data_chi, peakx, peaky, intensity = allres[1:6]
                CCDcalib = allres[-1]
                detectorparameters = allres[-2]
                # print('detectorparameters from file are: '+ str(detectorparameters))
                pixelsize = CCDcalib['pixelsize']
                CCDLabel = CCDcalib['CCDLabel']
                framedim = dictLT.dict_CCD[CCDLabel][0]
                dict_dp={}
                dict_dp['kf_direction']='Z>0'
                dict_dp['detectorparameters']=detectorparameters
                dict_dp['detectordistance']=detectorparameters[0]
                dict_dp['detectordiameter']=pixelsize*framedim[0]
                dict_dp['pixelsize']=pixelsize
                dict_dp['dim']=framedim
                dict_dp['peakX']=peakx
                dict_dp['peakY']=peaky
                dict_dp['intensity']=intensity
            
            if peak_detection_error:
                continue
            
            sorted_data = np.transpose(np.array([data_theta, data_chi]))
            tabledistancerandom = np.transpose(GT.calculdist_from_thetachi(sorted_data, sorted_data))

            codebars_all = []
            
            if len(data_theta) == 0:
                print("No peaks Found for : " + files)
                for intmat in range(matricies):
                    rotation_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                    strain_matrix[intmat][0][cnt,:,:] = np.zeros((3,3))
                    strain_matrixs[intmat][0][cnt,:,:] = np.zeros((3,3))
                    col[intmat][0][cnt,:] = 0,0,0
                    colx[intmat][0][cnt,:] = 0,0,0
                    coly[intmat][0][cnt,:] = 0,0,0
                    match_rate[intmat][0][cnt] = 0
                    mat_global[intmat][0][cnt] = 0
                        
                cnt += 1
                continue
            
            spots_in_center = np.arange(0,len(data_theta))

            for i in spots_in_center:
                spotangles = tabledistancerandom[i]
                spotangles = np.delete(spotangles, i)# removing the self distance
                # codebars = np.histogram(spotangles, bins=angbins)[0]
                codebars = histogram1d(spotangles, range=[min(angbins),max(angbins)], bins=len(angbins)-1)
                ## normalize the same way as training data
                max_codebars = np.max(codebars)
                codebars = codebars/ max_codebars
                codebars_all.append(codebars)
                
            ## reshape for the model to predict all spots at once
            codebars = np.array(codebars_all)
            ## Do prediction of all spots at once
            # prediction = model.predict(codebars)
            prediction = predict(codebars, wb, temp_key)
            max_pred = np.max(prediction, axis = 1)
            class_predicted = np.argmax(prediction, axis = 1)
            # print("Total spots attempted:"+str(len(spots_in_center)))
            # print("Took "+ str(time.time()-strat_time_P)+" seconds to predict spots")       
            predicted_hkl123 = classhkl[class_predicted]
            predicted_hkl123 = predicted_hkl123.astype(int)
            
            s_tth = data_theta * 2.
            s_chi = data_chi
            
            rotation_matrix1, mr_highest, mat_highest, \
                strain_crystal, strain_sample, iR_pix1, \
                            fR_pix1, spots_len1, best_match1 = predict_ubmatrix(seednumber, spots_in_center, classhkl, 
                                                                      hkl_all_class0, 
                                                                        hkl_all_class1, files,
                                                                        s_tth1=s_tth,s_chi1=s_chi,
                                                                        predicted_hkl1=predicted_hkl123,
                                                                        class_predicted1=class_predicted,
                                                                        max_pred1=max_pred,
                                                                        emin=emin,emax=emax,
                                                                        material_=material_, 
                                                                        material1_=material1_, 
                                                                        lim_y=lim_y, lim_x=lim_x, 
                                                                        cnt=cnt,
                                                                        dict_dp=dict_dp,
                                                                        rotation_matrix=rotation_matrix,
                                                                        mat_global=mat_global,
                                                                        strain_calculation=strain_calculation,
                                                                        ind_mat=ind_mat, 
                                                                        ind_mat1=ind_mat1,
                                                                        tolerance=tolerance,
                                                                        tolerance1 =tolerance1,
                                                                        matricies=matricies,
                                                                        tabledistancerandom=tabledistancerandom,
                                                                        text_file = text_file,
                                                                        try_previous1=try_previous1,
                                                                        mode_spotCycle = mode_spotCycle1,
                                                                        softmax_threshold_global123=softmax_threshold_global123,
                                                                        mr_threshold_global123=mr_threshold_global123,
                                                                        cap_matchrate123=cap_matchrate123,
                                                                        tolerance_strain123=tolerance_strain123,
                                                                        tolerance_strain1231=tolerance_strain1231,
                                                                        coeff123=coeff123,
                                                                        coeff_overlap=coeff_overlap,
                                                                        material0_limit=material0_limit, 
                                                                        material1_limit=material1_limit,
                                                                        model_direc=model_direc,
                                                                        use_previous_UBmatrix_name=use_previous_UBmatrix_name,
                                                                        material_phase_always_present=material_phase_always_present)
                
            for intmat in range(matricies):

                if len(rotation_matrix1[intmat]) == 0:
                    col[intmat][0][cnt,:] = 0,0,0
                    colx[intmat][0][cnt,:] = 0,0,0
                    coly[intmat][0][cnt,:] = 0,0,0
                else:
                    mat_global[intmat][0][cnt] = mat_highest[intmat][0]
                    self.mat_global[intmat][0][cnt] = mat_highest[intmat][0]
                    
                    final_symm =symmetry
                    if mat_highest[intmat][0] == 1:
                        final_symm = symmetry
                        final_crystal = crystal
                    elif mat_highest[intmat][0] == 2:
                        final_symm = symmetry1
                        final_crystal = crystal1
                    symm_operator = final_crystal._hklsym
                    # strain_matrix[intmat][0][cnt,:,:] = strain_crystal[intmat][0]
                    # strain_matrixs[intmat][0][cnt,:,:] = strain_sample[intmat][0]
                    self.strain_matrix[intmat][0][cnt,:,:] = strain_crystal[intmat][0]
                    self.strain_matrixs[intmat][0][cnt,:,:] = strain_sample[intmat][0]
                    # rotation_matrix[intmat][0][cnt,:,:] = rotation_matrix1[intmat][0]
                    self.rotation_matrix[intmat][0][cnt,:,:] = rotation_matrix1[intmat][0]
                    col_temp = get_ipf_colour(rotation_matrix1[intmat][0], np.array([0., 0., 1.]), final_symm, symm_operator)
                    # col[intmat][0][cnt,:] = col_temp
                    self.col[intmat][0][cnt,:] = col_temp
                    col_tempx = get_ipf_colour(rotation_matrix1[intmat][0], np.array([1., 0., 0.]), final_symm, symm_operator)
                    # colx[intmat][0][cnt,:] = col_tempx
                    self.colx[intmat][0][cnt,:] = col_tempx
                    col_tempy = get_ipf_colour(rotation_matrix1[intmat][0], np.array([0., 1., 0.]), final_symm, symm_operator)
                    # coly[intmat][0][cnt,:] = col_tempy
                    self.coly[intmat][0][cnt,:] = col_tempy
                    # match_rate[intmat][0][cnt] = mr_highest[intmat][0]    
                    self.match_rate[intmat][0][cnt] = mr_highest[intmat][0]
                    # spots_len[intmat][0][cnt] = spots_len1[intmat][0]    
                    self.spots_len[intmat][0][cnt] = spots_len1[intmat][0]
                    # iR_pix[intmat][0][cnt] = iR_pix1[intmat][0]    
                    self.iR_pix[intmat][0][cnt] = iR_pix1[intmat][0]
                    # fR_pix[intmat][0][cnt] = fR_pix1[intmat][0]    
                    self.fR_pix[intmat][0][cnt] = fR_pix1[intmat][0]
                    # best_match[intmat][0][cnt] = best_match1
                    self.best_match[intmat][0][cnt] = best_match1[intmat][0]
            cnt += 1
    
class LoggingCallback(Callback):
    """Callback that logs message at end of epoch.
    """
    def __init__(self, print_fcn, progress_func, qapp, model, fn_model):
        Callback.__init__(self)
        self.print_fcn = print_fcn
        self.progress_func = progress_func
        self.batch_count = 0
        self.qapp = qapp
        self.model = model
        self.model_name = fn_model
    
    def on_batch_end(self, batch, logs={}):
        self.batch_count += 1
        self.progress_func.setValue(self.batch_count)
        self.qapp.processEvents() 
        
    def on_epoch_end(self, epoch, logs={}):
        msg = "{Epoch: %i} %s" % (epoch, ", ".join("%s: %f" % (k, v) for k, v in logs.items()))
        self.print_fcn(msg)
        model_json = self.model.to_json()
        with open(self.model_name+".json", "w") as json_file:
            json_file.write(model_json)            
        # serialize weights to HDF5
        self.model.save_weights(self.model_name+"_"+str(epoch)+".h5")

def start():
    """ start of GUI for module launch"""
    app = QApplication(sys.argv)
    
    screen = app.primaryScreen()
    print('Screen: %s' % screen.name())
    size = screen.size()
    print('Size: %d x %d' % (size.width(), size.height()))
    rect = screen.availableGeometry()
    print('Available: %d x %d' % (rect.width(), rect.height()))
    
    win = Window(rect.width()//3, rect.height()//2)
    win.show()
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    start()