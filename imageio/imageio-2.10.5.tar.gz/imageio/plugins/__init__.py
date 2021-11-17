# -*- coding: utf-8 -*-
# imageio is distributed under the terms of the (new) BSD License.

# flake8: noqa

"""

Imagio is plugin-based. Every supported format is provided with a
plugin. You can write your own plugins to make imageio support
additional formats. And we would be interested in adding such code to the
imageio codebase!


What is a plugin
----------------

In imageio, a plugin provides one or more :class:`.Format` objects, and
corresponding :class:`.Reader` and :class:`.Writer` classes.
Each Format object represents an implementation to read/write a
particular file format. Its Reader and Writer classes do the actual
reading/saving.

The reader and writer objects have a ``request`` attribute that can be
used to obtain information about the read or write :class:`.Request`, such as
user-provided keyword arguments, as well get access to the raw image
data.


Registering
-----------

Strictly speaking a format can be used stand alone. However, to allow
imageio to automatically select it for a specific file, the format must
be registered using ``imageio.formats.add_format()``.

Note that a plugin is not required to be part of the imageio package; as
long as a format is registered, imageio can use it. This makes imageio very
easy to extend.


What methods to implement
--------------------------

Imageio is designed such that plugins only need to implement a few
private methods. The public API is implemented by the base classes.
In effect, the public methods can be given a descent docstring which
does not have to be repeated at the plugins.

For the Format class, the following needs to be implemented/specified:

  * The format needs a short name, a description, and a list of file
    extensions that are common for the file-format in question.
    These ase set when instantiation the Format object.
  * Use a docstring to provide more detailed information about the
    format/plugin, such as parameters for reading and saving that the user
    can supply via keyword arguments.
  * Implement ``_can_read(request)``, return a bool.
    See also the :class:`.Request` class.
  * Implement ``_can_write(request)``, dito.

For the Format.Reader class:

  * Implement ``_open(**kwargs)`` to initialize the reader. Deal with the
    user-provided keyword arguments here.
  * Implement ``_close()`` to clean up.
  * Implement ``_get_length()`` to provide a suitable length based on what
    the user expects. Can be ``inf`` for streaming data.
  * Implement ``_get_data(index)`` to return an array and a meta-data dict.
  * Implement ``_get_meta_data(index)`` to return a meta-data dict. If index
    is None, it should return the 'global' meta-data.

For the Format.Writer class:

  * Implement ``_open(**kwargs)`` to initialize the writer. Deal with the
    user-provided keyword arguments here.
  * Implement ``_close()`` to clean up.
  * Implement ``_append_data(im, meta)`` to add data (and meta-data).
  * Implement ``_set_meta_data(meta)`` to set the global meta-data.

"""

from ..core.imopen import imopen

try:
    import PIL
    from .pillow import PillowPlugin

    imopen.register_plugin("pillow", PillowPlugin)
except ImportError:
    pass  # Pillow not installed


# First import plugins that we want to take precedence over freeimage
from . import tifffile
from . import fits  # depends on astropy
from . import pillow_legacy
from . import grab

from . import freeimage
from . import freeimagemulti

from . import ffmpeg

from . import bsdf
from . import dicom
from . import npz
from . import swf

from . import feisem  # special kind of tiff, uses _tiffile
from . import simpleitk  # depends on itk or SimpleITK
from . import gdal  # depends on gdal

from . import lytro
from . import spe

from . import example

# Sort
import os
from .. import formats

formats.sort(*os.getenv("IMAGEIO_FORMAT_ORDER", "").split(","))
del os, formats
