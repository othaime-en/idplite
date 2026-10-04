"""
Outpost CLI Entry Point
"""

from importlib.metadata import PackageNotFoundError, version

import click

from outpost.commands.audit import audit
from outpost.commands.auth import auth
from outpost.commands.env import env
from outpost.commands.teams import teams

try:
    __version__ = version("outpost-cli")
except PackageNotFoundError:
    # Editable/unbuilt checkout (e.g. `python -m outpost.cli` straight from
    # a git clone with no `pip install` at all) — package metadata isn't
    # registered yet, so there's nothing real to report.
    __version__ = "0.0.0-dev"


@click.group()
@click.version_option(version=__version__, prog_name="outpost")
def cli():
    """Outpost — self-service environment provisioning from your terminal."""


cli.add_command(auth)
cli.add_command(env)
cli.add_command(audit)
cli.add_command(teams)


if __name__ == "__main__":
    cli()