"""This module handles the export of single FAST frames
"""

import logging

from PIL import Image

from ..tools.color_mapper import gray_to_rgb
from ..tools.frame_artists import label_image

log = logging.getLogger(__name__)


def image_writer(
    data, file_name, color_map, contrast, scaling=4, interp_order=3, text=None
):
    """Writes a gives 2D array to an image file

    Writes a given 2D array to an image file.

    Args:
        data: a 2D array with the frame data
        file_name: a string representing the output file name
        color_map: a valid ``matplotlib`` colormap
        contrast: the contrast specified as in ``tools.color_mapper.get_contrast_limits``
        scaling: a float representing the output scaling factor
        text: the text to be superimposed on the image, as in ``tools.frame_artists.label_image``

    Returns:
        nothing

    """
    rgb_data = gray_to_rgb(
        data,
        color_map=color_map,
        contrast=contrast,
        scaling=scaling,
        interp_order=interp_order,
    )
    if text is not None:
        rgb_data = label_image(rgb_data, text=text, font_size=0.04, border=0.01)
    img = Image.fromarray(rgb_data).convert("RGB")
    img.save(file_name)
    log.info("successfully written " + file_name)


def gsf_writer(data, file_name, metadata=None):
    """Write a 2D array to a Gwyddion Simple Field 1.0 file format

    Args:
        file_name: the name of the output (any extension will be replaced)
        data: an arbitrary sized 2D array of arbitrary numeric type
        metadata: (optional) a dictionary containing additional metadata to be included in the file

    Returns:
        nothing
    """

    x_res = data.shape[1]
    y_res = data.shape[0]

    data = data.astype("float32")

    if file_name.rpartition(".")[1] == ".":
        file_name = file_name[0 : file_name.rfind(".")]

    gsf_file = open(file_name + ".gsf", "wb")

    # prepare the metadata
    if metadata is None:
        metadata = {}
    metadata_string = ""
    metadata_string += "Gwyddion Simple Field 1.0" + "\n"
    metadata_string += "XRes = {0:d}".format(x_res) + "\n"
    metadata_string += "YRes = {0:d}".format(y_res) + "\n"
    for i in metadata.keys():
        try:
            metadata_string += i + " = " + "{0:G}".format(metadata[i]) + "\n"
        except:
            metadata_string += i + " = " + str(metadata[i]) + "\n"

    gsf_file.write(bytes(metadata_string, "UTF-8"))
    gsf_file.write(b"\x00" * (4 - len(metadata_string) % 4))
    gsf_file.write(data.tobytes(None))
    gsf_file.close()
    log.info("Successfully wrote " + file_name + ".gsf")
