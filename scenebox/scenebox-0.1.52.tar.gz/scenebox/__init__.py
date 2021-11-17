import os
root_dir = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(root_dir)

__version__ = "unknown"

file_1 = os.path.join(dir_path, "BASE_VERSION")
if os.path.exists(file_1):
    with open(file_1) as version_file:
        __version__ = version_file.readline()


file_2 = os.path.join(dir_path, "..", "..", "BASE_VERSION")
if os.path.exists(file_2):
    with open(file_2) as version_file:
        __version__ = version_file.readline()