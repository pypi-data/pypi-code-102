"""
Parent class for loading excavation shapefiles.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString, Polygon
import pandas as pd



class excavation_parent(gpd.GeoDataFrame):
    """
    The parent class for individual excavation types, i.e. tunnel, box, shaft, ribbon, walls
    """

    def __init__(self, excav_name, *args, **kwargs):
        """
        Build the class by using it on an existing geopandas geodataframe.
        """

        super().__init__(*args, **kwargs)

        self.excav_name = excav_name



    def replace_content(self, gdf):
        """
        Save a geodataframe to an excavation object by overwriting the content, since using 'self = ...' simply
        creates a local instance of the variable.
        """

        newcols = gdf.columns.difference(self.columns)
        oldcols = self.columns.difference(gdf.columns)

        self[newcols] = pd.NA
        self.drop(oldcols, axis=1, inplace=True)

        self[:] = pd.NA

        for i in gdf.index:
            self.loc[i] = gdf.loc[i]

        self.dropna(how='all', axis=0, inplace=True)
        self.dropna(how='all', axis=1, inplace=True)



    def export_to_txt(self, mask=None):
        """
        Parent method for exporting geodataframe information on excavations to text files serving as GRP input.
        """

        self.FORMAT = '{:.3f}'

        # if a mask is present, get the list of rows to use from that, otherwise use all rows
        if type(mask) == type(None):
            self.goodrows = self.index
        else:
            self.goodrows = self.index[mask]


