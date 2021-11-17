"""
Functions and classes for importing, processing and exporting tunnels and ribbons.
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString, Polygon
from .excavation_class import excavation_parent

# --------- FUNCTIONS ------------
# These global functions are used for both tunnels and ribbons



class tunnel_builder(excavation_parent):

    def __init__(self, excav_name, *args, **kwargs):

        super().__init__(excav_name, *args, **kwargs)


        # add the parameters for both ends if not present
        self.both_parameters()

        # split tunnels into individual segments,
        self.split_tunnels()


    def segments(self, curve):
        """
        Split a linestring into multiple linestrings defined by 2 points.

        Input:
            curve - shapely linestring or multilinestring

        Output:
            A list of split shapely linestrings
        """
        if type(curve) == LineString:
            return list(map(LineString, zip(curve.coords[:-1], curve.coords[1:])))
        else:  # multilinestring
            lines = []
            for c in list(curve):
                lines += list(map(LineString, zip(c.coords[:-1], c.coords[1:])))
            return lines


    def both_parameters(self):
        """
        Processes the values of trough width factor (K), volume loss (V) and diameter (D). For example, if a single
        column is provided (e.g K), it'll get copied as a constant to 'K1' and 'K2' for both sides of the tunnel.

        Input:
            geometry - geodataframe of shapely geometry

        Returns:
            the same geodataframe where the parameters at both ends of the tunnel are present
        """

        # process the parameters at either end of the tunnel
        names = list(set(self.columns).intersection(set(['V', 'K', 'D', 'r_width'])))
        for name in names:
            # if a single column is given for each parameter (x), copy it across to x1, x2.
            if name in self.columns:
                for i in [1, 2]:
                    self[f'{name}{i}'] = self[name]
                self.drop(name, axis=1, inplace=True) # drop the original name
            # if the x1 and x2 are given, but x2 contains any blanks, fill those blanks with corresponding x1
            else:
                ind_loc = np.where(np.isnan(self[f'{name}2']))[0]
                self.loc[ind_loc, f'{name}2'] = self.loc[ind_loc, f'{name}1']



    def split_tunnels(self):
        """
        Shapely linestrings can have more than 2 points, so split up the lines into segments. Depending on the complexity
        of the lines, this will create many more rows.

        Adjusts the parameters automatically to vary linearly across segments if the original full tunnel input is made
        to vary. If any parameters are blank for the 2nd parameter (e.g. K2), they are filled by the corresponding
        first parameter.

        Currently only works for the tunnel and ribbon geodataframes.

        Input:
            geometry - geodataframe of shapely geometry

        Returns:
            the same geodataframe where lines have been split into line segments
        """

        new_rows = []
        new_geometry = []

        set_names = list(set(self.columns.str[:-1]).intersection(set(['V', 'K', 'D', 'r_width'])))

        # if the tunnel parameters don't need to be processed, do a simpler, faster version
        if len(set_names) == 0:
            for i in range(self.shape[0]):
                line = self.loc[i]
                lines = self.segments(line['geometry'])
                temp_row = self.loc[i].copy()
                temp_row.drop('geometry', inplace=True)
                columns = temp_row.index
                temp_row = [temp_row for _ in range(len(lines))]
                new_rows += temp_row
                new_geometry += lines

        else:

            # split up the tunnels while interpolating the parameters

            for i in range(self.shape[0]):
                line = self.loc[i]
                lines = self.segments(line['geometry'])
                temp_row = self.loc[i].copy()

                temp_row.drop('geometry', inplace=True)
                columns = temp_row.index
                temp_row = [temp_row.copy() for _ in range(len(lines))]
                for j, l in enumerate(lines):
                    for p in range(2):
                        dist = line['geometry'].project(l.boundary[p], normalized=True)
                        for name in set_names:
                            temp_row[j][f'{name}{p + 1}'] = (1 - dist) * line[f'{name}1'] + dist * line[f'{name}2']
                new_rows += temp_row
                new_geometry += lines

        self.replace_content(gpd.GeoDataFrame(new_rows, columns=columns, geometry=new_geometry).reset_index())
        self.reset_index(inplace=True, drop=False)



    def export_to_txt(self, data_path, mask=None):
        """
        Save 3D linestring information to the file "tunnel.dat"at the nomiminated folder location.
        The z coordinates in the linestring represent the depth below ground level of the tunnel centre (axis).

        It is intended that a mask is created in the attribute gdf_mask so that only lines within or nearby a relevent
        grid are present.

        The settlement model parameters should be stored as columns in the geodataframe containing the linestrings.
        The column names are as follows:
            'V' - 0 for spandrel, 1 for concave curve
            'K' - corresponding user defined model (0 if not used)
            'D' - tunnel diameter
            'geometry' - shapely linestring (this column is present by default in a geodataframe)


        Note that GRP assumes each tunnel is a straight segment defined by 2 points. Therefore, this function breaks up
        the linestring into multiple segments accordingly. Therefore, if the variation of parameters described above were
        desired, a second set of V, K, D and r_width columns would be needed in the geodataframe, and each linestring would
        need to represent a single straight line segment. The function would need to be adjusted accordingly to use this
        additional information.

        Input:
            data_path - path to folder where box.dat is to be saved.
        Args:
            mask - a vector or series of booleans indicating which geometries to export
        """

        # boiler plate code (define format statement, get goodrows based on input mask)
        super().export_to_txt(mask)

        # extract coordinates from lines
        coords = [np.array(self.iloc[t].geometry) for t in self.goodrows]
        coords = np.array(coords)

        # get parameters to save to file, based on whether it's a tunnel or ribbon
        # these need to be in the precise order given here
        if 'r_width1' in self.columns:
            params = [['V1', 'K1', 'D1', 'r_width1'], ['V2', 'K2', 'D2', 'r_width2']]
        else:
            params = [['V1', 'K1', 'D1'], ['V2', 'K2', 'D2']]


        # open the file and save the data
        with open(data_path + self.excav_name + '.dat', 'w') as tunnel_file:
            for i, row in enumerate(self.goodrows):
                temp = self.iloc[row]
                values = coords[i, 0].tolist() + temp.loc[params[0]].tolist() + coords[i, 1].tolist() + temp.loc[
                    params[1]].tolist()

                # format it to have reasonable significant figures
                values = [self.FORMAT.format(j) for j in values]
                tunnel_file.write('\t'.join(values) + '\n')




# tunnel = tunnel_builder(r'C:\GRP\v5_input\tunnel.shp')
#
# tunnel.export_to_txt(r'C:\GRP\v5_output\\')
