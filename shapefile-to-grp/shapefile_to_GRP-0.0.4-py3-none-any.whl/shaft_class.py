"""
Functions and classes for importing, processing and exporting shafts, represented by a point.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString, Polygon
import pandas as pd
from .excavation_class import excavation_parent

class shaft_builder(excavation_parent):

    def __init__(self, excav_name, *args, **kwargs):

        super().__init__(excav_name, *args, **kwargs)

        self.create_circle()


    def create_circle(self):
        """
        Convert shafts into polygons covering their true area. The shaft point is later taken as the polygon's
        centroid.
        """

        self['Z'] = [g.z for g in self['geometry']] # save elevation explicitly
        temp_geom = []
        for i, row in self.iterrows():
            temp_geom.append(row['geometry'].buffer(row['R']))
        self['geometry'] = temp_geom


    def export_to_txt(self, data_path, mask=None):
        """
        Save 3D point information to the file "shaft.dat" at the nomiminated folder location. The z coordinates in the
        point represent the depth below ground level. This is intended for circular open excavations.

        The settlement model parameters should be stored as columns in the geodataframe containing the points.
        The column names are as follows (names on far right correspond to GRP manual):
            'model' - 0 for spandrel, 1 for concave curve, 2 for parabolic curve with horizonal movements (3)
            'model_num' - corresponding user defined model (0 if not used)
            'V' - dv/Z ratio of excavation
            'W' - W/Z ratio of excavation
            'H' - dh/dv ratio of excavation
            'Z' - depth of shaft below ground
            'radius' - the shaft radius
            'geometry' - shapely point (this column is present by default in a geodataframe)

        Input:
            data_path - path to folder where box.dat is to be saved.
        Args:
            mask - a vector or series of booleans indicating which geometries to export
        """

        # boiler plate code (define format statement, get goodrows based on input mask)
        super().export_to_txt(mask)

        with open(data_path + 'shaft.dat', 'w') as f:
            for i, row in enumerate(self.goodrows):  # loop through each shaft

                # shafts are represented by polygons, so take the centroid
                point = self.iloc[row].geometry.centroid
                temp = self.iloc[row]

                values = [point.x, point.y, temp.Z, temp.R, temp.V, temp.W, temp.H, temp.model, temp.model_num]
                values = [self.FORMAT.format(i) for i in values]
                f.write('\t'.join(values) + '\n')