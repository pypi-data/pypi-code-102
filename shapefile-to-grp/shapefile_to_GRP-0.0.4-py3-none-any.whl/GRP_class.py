"""
The main overall class, which contains references to the grid class, excavation classes, and overall settings
"""

from .tunnel_class import tunnel_builder
from .box_class import box_builder
from .shaft_class import shaft_builder
from .wall_class import wall_builder
from .grid_class import grid_builder
from .model_class import model_builder
import geopandas as gpd

class excavation_builder(dict):
    """
    A class that holds all the excavation information.
    """

    # information describing the class name for each excavation type
    class_funcs = {
        'box': box_builder,
        'tunnel': tunnel_builder,
        'ribbon': tunnel_builder,
        'shaft': shaft_builder,
        'walls': wall_builder
    }

    def __init__(self, excavation_files, input_path, model_names=[], *args, **kwargs):
        """
        Load in excavation-related information including models (if any).

        Input:
            excavation_files - A dictionary linking a shapefile name (excluding extension) with an excavation type.
                Must use one of: box, tunnel, ribbon, shaft, walls
            input_path - path to directory where input files are located
            model_names - list of csv file names (including extension) that contain user-defined files. Empty list if none exist.
        """
        # load in excavation geometry

        super().__init__(*args, **kwargs)

        self.excavation_files = excavation_files
        for key in self.excavation_files.keys():
            gdf = gpd.read_file(input_path + self.excavation_files[key] + '.shp')
            self[key] = self.class_funcs[key](key, gdf)

        self.models = model_builder(model_names=model_names, input_path=input_path)


    def export_geometry(self, grid, output_path):
        """
        Export the geometry and grid information to GRP text file inputs, one set for each grid using only excavations
        near the grid.
        Currently saves to a single file name so the data overwrites itself.

        Input:
            grid - initiated grid object from grid_builder class
            output_path - path to where GRP input files will be stored
        """


        # export models file
        self.models.export_models(output_path)

        numgrids = len(grid.grids)

        # loop through grids and export grid file
        for gridnum in range(numgrids):
            grid.export_grid(output_path, grid.run_mode, grid.imperial, grid.analysis_name, gridnum)
            # loop through and export each excavation
            for excavation in self.values():
                mask = grid.geometry_near_grid(gdf=excavation, gridnum=gridnum)
                excavation.export_to_txt(data_path=output_path, mask=mask)



if __name__ == '__main__':
    excavations = excavation_builder({'box':'box', 'tunnel':'tunnels'}, input_path='C:/GRP/example_input/', model_names=[])
    grids = grid_builder(500, 50, 50, excavations)
    excavations.export_geometry(grids, output_path='C:/GRP/example_output/')


