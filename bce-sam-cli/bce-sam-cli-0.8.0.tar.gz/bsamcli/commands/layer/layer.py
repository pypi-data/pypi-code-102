"""
Command group for "layer" suite for commands. It provides common CLI arguments, template parsing capabilities,
setting up stdin/stdout etc
"""

import click

from .init.cli import cli as init_cli


@click.group()
def cli():
    pass  # pragma: no cover


# Add individual commands under this group
cli.add_command(init_cli)