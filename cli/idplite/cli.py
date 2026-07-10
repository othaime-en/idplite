"""
IDP Lite CLI Entry Point
"""

import click

from idplite.commands.auth import auth


@click.group()
@click.version_option(version="0.1.0", prog_name="idplite")
def cli():
    """IDP Lite — self-service environment provisioning from your terminal."""


cli.add_command(auth)


if __name__ == "__main__":
    cli()