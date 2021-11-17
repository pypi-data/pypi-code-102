#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Runs an example of TLSeparation for a single tree point cloud.

@author: Dr. Matheus Boni Vicari
"""

import numpy as np # Imports numpy to load and export point clouds saved in a .txt format
import tlseparation as tls # Imports tlseparation with a shortened nickname 'tls'

path_to_cloud_file = 'example_tree.txt'

# If the data is delimited by commas, use the line below:
point_cloud = np.loadtxt(path_to_cloud_file)
# Otherwise, comment the line above and uncomment the line below (remove the first #):
#point_cloud = np.loadtxt(path_to_cloud_file, delimiter=' ') # Replace the delimiter inside the single quotes to match the one used in the point cloud

point_cloud = point_cloud[:, :3] # limits the data to the first three columns (x, y, z)

# Runs the separation using the 'generic_tree' script.
wood, leaf = tls.scripts.generic_tree(point_cloud)

# OPTIONAL
# It's possible to run a post-processing filter that might improve the results.
# For that, uncommnet the lines below:
#wood1, not_wood = tls.scripts.isolated_clusters(wood)
#wood = wood1
#leaf = np.vstack((leaf, not_wood))

# Saving the results:
np.savetxt('example_wood.txt', wood, fmt='%1.3f')
np.savetxt('example_leaf.txt', leaf, fmt='%1.3f')