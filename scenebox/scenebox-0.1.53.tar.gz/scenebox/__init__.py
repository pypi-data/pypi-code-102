import os
root_dir = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(root_dir)

if os.path.exists(os.path.join(dir_path, "BASE_VERSION")):
    with open(os.path.join(dir_path, "BASE_VERSION")) as version_file:
        __version__ = version_file.readline()
elif os.path.exists(os.path.join(dir_path, "..", "..", "BASE_VERSION")):
    with open(os.path.join(dir_path, "..", "..", "BASE_VERSION")) as version_file:
        __version__ = version_file.readline()

else:
    __version__ = "unknown"