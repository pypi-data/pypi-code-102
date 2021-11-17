"""
Functions and classes for importing, processing and exporting boxes.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString, Polygon
import pandas as pd
from .excavation_class import excavation_parent


class wall_builder(excavation_parent):
    def __init__(self, excav_name, *args, **kwargs):

        super().__init__(excav_name, *args, **kwargs)

        self.process_box_vertices()




    def export_to_txt(self, data_path, mask=None):
        """
        Save 3D linestring information to the file "walls.dat" at the nomiminated folder location. The z coordinates in the
        line represent the depth below ground level. The settlement is calculated on the side nearest the observer when
        looking at the wall with the start point on the left.
        Multiple walls can be used to create a box excavation that allows for end effects and superposition of settlement
        for closed corners and uses a concave curve only.


        The settlement model parameters should be stored as columns in the geodataframe containing the points.
        The column names are as follows (names on far right correspond to GRP manual):
            'V' - dv/Z ratio of excavation
            'H' - dh/dv ratio of excavation
            'iM' - the point of inflexion figure on the wall side. For Hseih and Ou model, use 0.42465
            'iP' – the point of inflexion on the opposite side. For Hsieh and Ou model use 0.699
            'geometry' - shapely linestring (this column is present by default in a geodataframe)

        Note: each linestring should be a straight line defined by 2 points. The z coordinate of both points should be
        identical (only the first is used).

        Input:
            data_path - path to folder where walls.dat is to be saved.
        Args:
            mask - a vector or series of booleans indicating which geometries to export
        """

        # boiler plate code (define format statement, get goodrows based on input mask)
        super().export_to_txt(mask)

        with open(data_path + self.excav_name + '.dat', 'w') as f:
            for i, row in enumerate(self.goodrows):  # loop through each wall

                coords = np.array(self.iloc[row].geometry)  # get coordinates of line as numpy array

                if coords.shape[0] > 2:
                    print('warning, too many points in linestring for walls.dat, only using first two')

                values = [coords[0, 0], coords[0, 1], coords[1, 0], coords[1, 1], coords[0, 2],
                          self.iloc[row].V, self.iloc[row].H, self.iloc[row].iM, self.iloc[row].iP]
                values = [self.FORMAT.format(i) for i in values]
                f.write('\t'.join(values) + '\n')
