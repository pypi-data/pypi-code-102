"""
Functions and classes for importing, processing and exporting boxes.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString, Polygon
import pandas as pd
from .excavation_class import excavation_parent

class box_builder(excavation_parent):



    def __init__(self, excav_name, *args, **kwargs):


        super().__init__(excav_name, *args, **kwargs)

        self.process_box_vertices()




    def process_box_vertices(self):
        """
        Make sure that boxes are graphically represented by a polygon, and internally represented as a geodataframe of
        points and associated attributes. I.e. get a polygon from points input and get points from polygon input.

        The 'geometry' column will contain the effective geometry; the box polygon. All point geometry and
        associated settlement attributes are stored as lists in a new 'GRP_points' column.

        """


        # create the polygons if the geodataframe contains points
        if type(self.loc[0, 'geometry']) == Point:
            temp_geom = []
            grp_points = []
            box_attributes = []

            names = list(set(self['name']))  # get list of unique names
            # loop through excavations
            for i, name in enumerate(names):
                temp = self[self['name'] == name].copy()
                box_attributes.append([temp.iloc[0].model, temp.iloc[0].model_num])
                temp.drop(['model', 'model_num'], axis=1, inplace=True)  # these are per-box, not per wall
                temp.sort_values(by='order', inplace=True)
                temp = temp.append(temp.iloc[0])
                temp_geom.append(Polygon(LineString(temp.geometry.tolist())))

                # if not anti-clockwise, reverse their order
                if not temp_geom[-1].exterior.is_ccw:
                    temp = temp[::-1]
                    temp_geom[-1] = Polygon(LineString(temp.geometry.tolist()))
                temp.reset_index(inplace=True, drop=True)
                grp_points.append(temp)

            self.replace_content(gpd.GeoDataFrame(box_attributes, columns=['model', 'model_num'], geometry=temp_geom))


            self['GRP_points'] = grp_points


        else:

            raise('Box polygon input not yet fully implemented')

            if not 'name' in self.columns:
                self['name'] = self.index
                


    def export_to_txt(self, data_path, mask=None):
        """
        Export box information stored as a geodataframe of parameters, with an additional 'GRP_points' column, where each
        element is itself a geodataframe of box corner information.

        The settlement model parameters should be stored as columns in the geodataframe containing the polygons.
        The column names are as follows (names on far right correspond to GRP manual):
            'model' - 0 for spandrel, 1 for concave curve                               - P
            'model_num' - corresponding user defined model (0 if not used)              - Q
            'geometry' - shapely polygon (this column is present by default in a geodataframe)
            'GRP_points' a column where each row points to a separate geopandas geodataframe representing information at a
                wall vertex. It contains the columns:
                'V' - dv/Z ratio of excavation (%)                                          - Vx
                'W' - W/Z ratio of excavation                                               - Wx
                'H' - dh/dv ratio of excavation                                             - Hx
                'geometry' - shapely point (this column is present by default in a geodataframe)


        Input:
            data_path - path to folder where box.dat is to be saved.
        Args:
            mask - a vector or series of booleans indicating which geometries to export
        """

        # boiler plate code (define format statement, get goodrows based on input mask)
        super().export_to_txt(mask)

        with open(data_path + self.excav_name + '.dat', 'w') as f:

            f.write(f'{len(self.goodrows)}\n')

            # loop through excavations
            for i, row in enumerate(self.goodrows):

                f.write(f"{self.loc[row, 'GRP_points'].shape[0] - 1}\t{self.model.iloc[row]}\t{self.model_num.iloc[row]}\n")

                # loop through walls in excavation
                for p in range(len(self.loc[i, 'GRP_points']) - 1):
                    point1 = self.loc[row, 'GRP_points'].iloc[p]
                    point2 = self.loc[row, 'GRP_points'].iloc[p + 1]

                    values = [point1.geometry.x, point1.geometry.y, point1.geometry.z, point1.V, point1.W,
                              point2.geometry.x, point2.geometry.y, point2.geometry.z, point2.V, point2.W, point1.H]

                    values = [self.FORMAT.format(i) for i in values]
                    f.write('\t'.join(values) + '\n')


    def process_overlapping_polygons(all_geometry, to_convert):
        """
        NOTE, THIS CURRENTLY ONLY WORKS FOR BOXES DEFINED AS POLYGONS, NOT POINTS. I'VE THEREFORE NOT BOTHERED TO
        IMPLEMENT THIS YET - DO NOT USE

        This function is to facilitate adjacent open excavations of different depths. It assumes that the shallow excavation
        also covers the full area of the deep one, such that a polygon with shallow excavation and negative settlement should
        be created.

        Note: this currently only checks the 'box' item in the geometry dictionary, since that's the only one that has
        shapely polygons.
        If any of the boxes are defined by points, the overlapping processing is NOT applied.

        Input:
            all_geometry - a dictionary of geodataframe of shapely polygons, linestrings or points
            to_convert - True if the elevations are to be converted to depth below ground level
        """

        if to_convert:  # if z coords are given as reduced level, the shallow ones are maximized
            function = max
            function2 = np.argmax
        else:  # otherwise if it's provided as depth below ground level, you want to minimize
            function = min
            function2 = np.argmin

        new_rows = []
        new_polygons = []

        # loop through all available geodataframes and proceed if the first one is a polygon

        if 'box' in all_geometry.keys():

            # don't do the overlapping algorithm if any of the boxes are defined as points
            # TODO: this could probably be improved in the future to work with mixed point and polygon definitions
            if 'GRP_points' in all_geometry['box'].columns:
                return all_geometry

            geometry = all_geometry['box']
            for i in range(geometry.shape[0] - 1):
                for j in range(i + 1, geometry.shape[0]):
                    if geometry.loc[i, 'geometry'].overlaps(geometry.loc[j, 'geometry']):
                        # create a new polygon of the overlapping area
                        new_poly = geometry.loc[i, 'geometry'].intersection(geometry.loc[j, 'geometry'])
                        # get the mean elevation of the two original polygons
                        mean_z1 = np.array(geometry.loc[i, 'geometry'].exterior.coords)[:, 2].mean()
                        mean_z2 = np.array(geometry.loc[j, 'geometry'].exterior.coords)[:, 2].mean()
                        # get the polygon's x/y coords
                        poly_coords = np.array(new_poly.exterior.coords)[:, :2]
                        # get the mean elevation of the shallower excavation
                        mean_z = np.ones(poly_coords.shape[0]) * function(mean_z1, mean_z2)
                        # set the vertical coordinates as the shallow ones
                        new_poly = Polygon(np.stack((poly_coords[:, 0], poly_coords[:, 1], mean_z), axis=1).tolist())

                        # copy the attributes from the deeper original polygon
                        which_deeper = function2([mean_z1, mean_z2])
                        temp_row = geometry.loc[[i, j][which_deeper]].copy()
                        temp_row.drop('geometry', inplace=True)
                        temp_row['V'] *= -1  # make the settlement negative
                        new_polygons.append(new_poly)
                        new_rows.append(temp_row.to_list())

            if len(new_rows) > 0:

                new_polys = gpd.GeoDataFrame(new_rows, columns=temp_row.index, geometry=new_polygons)

                all_geometry['box'] = pd.concat((geometry, new_polys))
                # for some reason this 'level_0' column is added, so delete it
                if 'level_0' in all_geometry['box'].columns:
                    all_geometry['box'].drop('level_0', axis=1, inplace=True)
                all_geometry['box'].reset_index(inplace=True, drop=True)

        return all_geometry


# tunnel = box_builder(r'C:\GRP\example_input\boxes_points.shp')
#
# tunnel.export_to_txt(r'C:\GRP\v5_output\\')
