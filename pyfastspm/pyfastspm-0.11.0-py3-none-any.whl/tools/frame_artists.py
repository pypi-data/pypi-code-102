"""Utilities for drawing and writing stuff on frames before exporting."""

import logging

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pkg_resources import resource_filename

log = logging.getLogger(__name__)


def label_image(rgb_image, text=None, font_size=0.05, border=0.01):
    """

    Superimposes the given text on an RGB image, at a chosen position.

    Args:
        rgb_image: an RGB ndarray as the input image
        text: a dictionary where the keys are the text to be written and the values are the corresponding
            positions on the image. Accepted values for text positioning are ``top-left``,
            ``top-right``, ``bottom-left``, ``bottom-right``, ``center``
        font_size: the fraction of the image width/height to be used as font height
        border: the fraction of the image width/height to be left as border

    Returns:
        an RGB ndarray

    Examples:
        >>> image_with_labels = label_image(my_rgb_image, {'Graphene edges':'top-right', 'T = 453K':'bottom-right'})

    """
    image = Image.fromarray(rgb_image).convert("RGBA")
    txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    font = ImageFont.truetype(
        resource_filename("pyfastspm.tools.resources.fonts", "OpenSans-Semibold.ttf"),
        int(image.size[0] * font_size),
    )
    for txt_label in text.keys():
        if text[txt_label] == "top-left":
            x_pos = image.size[0] * border
            y_pos = image.size[1] * border
        elif text[txt_label] == "top-right":
            x_pos = image.size[0] * (1 - border) - font.getsize(txt_label)[0]
            y_pos = image.size[1] * border
        elif text[txt_label] == "center":
            x_pos = 0.5 * (image.size[0] - font.getsize(txt_label)[0])
            y_pos = 0.5 * (image.size[1] - font.getsize(txt_label)[1])
        elif text[txt_label] == "bottom-left":
            x_pos = image.size[0] * border
            y_pos = image.size[1] * (1 - border) - font.getsize(txt_label)[1]
        elif text[txt_label] == "bottom-right":
            x_pos = image.size[0] * (1 - border) - font.getsize(txt_label)[0]
            y_pos = image.size[1] * (1 - border) - font.getsize(txt_label)[1]
        else:
            raise ValueError("invalid specification of text position")
        draw.text((x_pos, y_pos), txt_label, fill=(255, 255, 255, 180), font=font)
    return np.array(Image.alpha_composite(image, txt))[:, :, :3]
