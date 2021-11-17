# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


import typer
import platform

from elangai import __version__
from elangai.template import APP_GENERATOR
from elangai.model import (
    ModelConverter,
    ModelDissector
)


app = typer.Typer()


@app.command()
def model_dissector(model_path: str):
    """Show the input and output tensor information from the source file.

    :param model_path: path to the AI model file
    """
    dissector = ModelDissector(model_path)
    dissector.dissect()


@app.command()
def model_converter(src: str = typer.Option(..., "--src", help='path to the source file'),
                    dst: str = typer.Option(..., "--dst", help='path to desired output of the converted model, the ``.trt`` file'),
                    precision: str = typer.Option('fp32', "--precision", "-p", help='precision for the AI model parameter')):
    """Convert AI model from source file to ``.trt`` file.
    """
    converter = ModelConverter(src, dst, precision)
    converter.convert()


@app.command()
def generate(app_name: str):
    """Generate ``elangai`` app.

    :param app_name: ``elangai`` app name
    """
    APP_GENERATOR[app_name]


@app.command()
def version():
    """Show the version of ``elangai``.
    """
    typer.echo("elangai info -- version: {}, "
               "python: {}, "
               "platform: {}".format(__version__,
                                     platform.python_version,
                                     str(platform.system()).lower()))


if __name__ == '__main__':
    app()
