"""
Functions and information regarding the GRP grids
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point, LineString, Polygon, GeometryCollection
import pandas as pd




class grid_builder(object):


    def __init__(self, max_dim, min_dist, edge_buffer, excavations, run_mode=1, imperial=False, analysis_name='run'):
        """

        Input:
            max_dim - maximum width or height of a grid
            min_dist - minimum distance between any excavation and the edge of a grid
            edge_buffer - the distance to expand the grid so as to include nearby excavations in the analysis
            excavations - dictionary of pandas geodataframes of excavation geometry
        Args:
            run_mode - the GRP run mode
            imperial - False if metric system (default), or True if imperial system
            analysis_name - name of the current analysis
        """

        # set required parameters
        self.max_dim = max_dim
        self.min_dist = min_dist
        self.edge_buffer = edge_buffer
        self.run_mode = run_mode
        self.imperial = imperial
        self.analysis_name = analysis_name


        # get the grids
        self.return_grid(excavations)


    def geometry_near_grid(self, gdf, gridnum):
        """
        Create a mask for excavations based on their proximity to a grid.

        Input:
            gdf - a geodataframe of excavation geometry
            gridnum - index of the grid being assessed
        """

        distances = gdf.distance(self.grids.iloc[gridnum])

        mask = distances <= self.edge_buffer

        return mask






    def return_grid(self, excavations):
        """
        Grid analysis:
        Create the grids covering the excavation, representing where GRP analysis takes place. Each individual grid is an
        independant GRP analysis.

        The script will attempt to automatically create a suitable set of grids based on the extent
        of the provided geometry. In the main processing function, each grid will only be processed for the geometry within
        it or otherwise nearby.

        It works by subdividing the area covering the full geometry (+ buffer zone around all 4 sides of the rectangle) into
        a grid of smaller rectangles based on the max_dim parameter. Grids which are outside the zone of influence are
        removed from the analysis. Grids within the zone of influence are truncated to the buffer zone from the geometry,
        resulting in fairly optimal coverage.

        Note that smaller max_dim values create a larger number of fine grids to cover the geometry, which results in less
        wastage in the GRP processing and higher efficiency. However, keep in mind that geometry from outside the grid but
        within the buffer distance of the grid must also be included in the analysis, meaning that this exterior geometry
        must be assessed in more than one grid, and that having too fine a grid size will increase this redundant assessment
        thereby reducing efficiency.


        Returns:
            Adds a geoseries of grids to the object.
        """

        # import matplotlib.pyplot as plt
        # fig, ax = plt.subplots()

        if len(excavations) == 0:
            raise Exception('Error: there is no excavation. Check shapefiles or ensure analysis window is appropriate.')

        # get the minimum rectangles around each excavation, stored as a dataframe of minx, miny, maxx, maxy coords
        bounds = pd.DataFrame()
        for key in excavations.keys():
            bounds = pd.concat((bounds, excavations[key].bounds))

        # expand the rectangles by the min_dist between excavation and grid edge
        bounds[['minx', 'miny']] -= self.min_dist
        bounds[['maxx', 'maxy']] += self.min_dist

        # get extents of the overall, combined geometry
        bound_coords = np.concatenate((
            np.floor(bounds.min()[['minx', 'miny']]),
            np.ceil(bounds.max()[['maxx', 'maxy']]))
        ).astype('i8')

        # get lower points in format that can be added to bound_coords later
        lower_points = np.concatenate((bound_coords[:2], bound_coords[:2]))

        # get the size of the overall area in each dimension
        extents = np.array([bound_coords[2] - bound_coords[0], bound_coords[3] - bound_coords[1]])
        # get the number of grids along each dimension required to satisfy the maximum grid size
        num_grids = np.ceil(extents/self.max_dim).astype('i8')

        # combine all excavations into a single geometry collection to calculate distances
        geometry = GeometryCollection()
        for key in excavations.keys():
            geometry = GeometryCollection(list(geometry) + excavations[key].geometry.to_list())
        # create buffered geometry to use in trimming down grids to their smallest extent
        geometry_buffered = geometry.buffer(distance=self.min_dist)
        #gpd.GeoSeries(geometry).plot(ax=ax, color='g')



        # --- loop through potential grids, discard ones which are too far away, and shrink down the remainders ----
        output = []
        for x in range(num_grids[0]): # loop through grids in x dimension
            for y in range(num_grids[1]): # loop through grids in y dimension
                # bounds of current grid
                sub_bounds = np.array((x * self.max_dim, y * self.max_dim, (x + 1) * self.max_dim, (y + 1) * self.max_dim)) + lower_points
                sub_bounds = pd.Series(sub_bounds, index=['minx', 'miny', 'maxx', 'maxy'])


                # check whether the smaller grid extent exceeds the original grid (might happen on the last ones)
                exceeded_max = sub_bounds[2:] > bound_coords[2:]
                sub_bounds[2:][exceeded_max] = bound_coords[2:][exceeded_max]
                # create shapely polygon of grid
                grid_poly = LineString([sub_bounds[:2], sub_bounds[2:]]).envelope


                # if the minimum distance from the current grid to the geometery is less than the buffer distance,
                # don't bother using the current grid
                if geometry.distance(grid_poly) > self.min_dist:
                    continue

                # find area surrounding buffer zone of geometry within the grid
                overlap = geometry_buffered.intersection(grid_poly).envelope

                # if the overlap is a single point (i.e. just touching), don't bother with grid
                if type(overlap) == Point:
                    continue

                if overlap.is_empty:
                    print("Error: this shouldn't happen due to the if statements above, so if it does something weird is happening")
                    continue

                # find intersection of the two grids (i.e. the truncated one)
                # this is important for shrinking the grid to the smallest allowable size
                new_grid = grid_poly.intersection(overlap)

                # rebuild grid with rounded coords
                grid_poly = LineString([sub_bounds[:2], sub_bounds[2:]]).envelope


                output.append(grid_poly)

        self.grids = gpd.GeoSeries(output)


    def plot_grid_extents(self):
        """
        NOTE: THIS WILL NEED TO BE ADAPTED TO MOATA

        Plot the grid extents over the geometry, to check coverage and overlap.
        """


        # plot the grids as transparent rectangles
        self.grids.plot(color='C0', alpha=0.5, edgecolor='None')

        # plot bigger grids which show the grid proximity zone for which excavations are considered
        self.grids.buffer(self.edge_buffer).plot(color='m', alpha=0.1, edgecolor='None')


    def export_grid(self, output_path, run_mode, imperial, analysis_name, gridnum):
        """
        Save a single grid to a GRP input file

        Inputs:
            gridnum - index of the current grid
            data_path - path to where grid.dat will be stored

        """

        FORMAT = '{:.3f}'

        # save grid file
        with open(output_path + 'grid.dat', 'w', newline='') as grid_file:

            grid_file.write(f"{run_mode}\t{int(imperial)}\n")

            bounds = self.grids.iloc[gridnum].bounds

            values = [FORMAT.format(i) for i in bounds]
            grid_file.write('\t'.join(values) + f"\t{analysis_name}_{gridnum}\n")

        print()


# class parent(gpd.GeoDataFrame):
#     pass
#
# class tunnels(parent):
#     def __init__(self, gdf):
#
#         super().__init__(gdf)
#
#
#         #self.doubleV()
#
#     def doubleV(self):
#         self['V'] *= 2
#
# result = tunnels( gpd.read_file('C:/GRP/example_input/tunnels.shp'))
#

