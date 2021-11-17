"""
Class for handling user-defined settlement models. Loads them and saves them in a GRP-appropriate input format.
"""

import numpy as np

class model_builder:

    def __init__(self, model_names, input_path, skiprows=0):
        """
        Load user-defined models to models.dat in the nominated folder. The model points are interpolated with
        cubic splines. Format should be CSV files.

        Note that GRP sometimes doesn't play nicely when there are zero model files, so one is defined by default if
        no model files are given.

        Each model is defined by 3 columns:
        x - normalised (to wall depth) distance from the wall)
        V - normalised (to maximum) vertical movements
        H - normalised (to maximum) horizontal movements

        Input:
            model_names - a list of model names
            data_path - the path to the folder where the models are located.
        Args:
            skiprows - number of rows to skip (default 0). For example, use 1 if there is a row of headings.
        """

        self.models = []
        for name in model_names:
            self.models.append(np.loadtxt(input_path + name, skiprows=skiprows, delimiter=','))

        if len(model_names) == 0:
            models = [np.array([[0., 0.5, 0.5],
                                [0.375, 1., 1.],
                                [0.75, 0.7, 0.7],
                                [1.125, 0.3, 0.3],
                                [1.5, 0.1, 0.1],
                                [1.875, 0.043, 0.043],
                                [2.25, 0.023, 0.023],
                                [2.625, 0.01, 0.01],
                                [3., 0., 0.]])]

        return models

    def export_models(self, output_path):
        """
        Export user-defined models to models.dat in the nominated folder. The model points are interpolated with
        cubic splines.

        Each model is defined by an [n x 3] numpy array of n data points and 3 columns.
        The columns are:
        x - normalised (to wall depth) distance from the wall)
        V - normalised (to maximum) vertical movements
        H - normalised (to maximum) horizontal movements

        Input:
            data_path - the path to the folder where models.dat will be saved.
        """

        with open(output_path + 'models.dat', 'w') as f:
            f.write(f'{len(self.models)}\n')

            for model in self.models:    # loop through models
                f.write(f'{model.shape[0]}\n')

                for i in range(model.shape[0]): # loop through model points
                    vals = ['{:.5f}'.format(j) for j in model[i]]
                    f.write('\t'.join(vals) + '\n')


