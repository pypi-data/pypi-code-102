# -*- coding: utf-8 -*-
"""
Init command to scaffold a project app from a template
"""
import logging
import click

from bsamcli.cli.main import pass_context, common_options
from bsamcli.commands.local.generate_event.cli import HELP_TEXT
from bsamcli.local.init import generate_layer_project
from bsamcli.local.init import LAYER_RUNTIME_TEMPLATE_MAPPING
from bsamcli.local.init.exceptions import GenerateProjectFailedError
from bsamcli.commands.exceptions import UserException

LOG = logging.getLogger(__name__)
LAYER_SUPPORTED_RUNTIME = [r for r in LAYER_RUNTIME_TEMPLATE_MAPPING]

HELP_TEXT = """
Create a demo repository for layer.\n

Examples:\n

$ bsam layer init --name mylayer --compatible-runtimes python3

$ bsam layer init -n mylayer -r python3

$ bsam layer init -n mylayer -r python3 -r python2

$ bsam layer init -n mylayer -r python3 -r python2 -o my_layer_dir/

"""

@click.command(name="init",  help=HELP_TEXT, context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.option('-n', '--name', default="demo-layer", help="Name of your layer and the folder to be generated")
@click.option('-r', '--compatible-runtimes', multiple=True, type=click.Choice(LAYER_SUPPORTED_RUNTIME), default="nodejs10,nodejs12",
              help="Compatible runtimes of your layer")
@click.option('-o', '--output-dir', default='.', type=click.Path(), help="Where to output the initialized layer into")
@common_options
@pass_context
def cli(ctx, name, compatible_runtimes, output_dir):
    # All logic must be implemented in the `do_cli` method. This helps ease unit tests
    do_cli(ctx, name, compatible_runtimes, output_dir)  # pragma: no cover


def do_cli(ctx, name, compatible_runtimes, output_dir):
    """
    Implementation of the ``cli`` method, just separated out for unit testing purposes
    """
    LOG.debug("Layer init command")
    click.secho("[+] Initializing layer project structure...", fg="green")

    try:
        generate_layer_project(name, compatible_runtimes, output_dir)        
        click.secho("[*] Layer project initialization is now complete", fg="green")
    except GenerateProjectFailedError as e:
        raise UserException(str(e))
