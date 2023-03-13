from datetime import datetime

import click

from edxbackup.bookkeeping import DEFAULT_RETENTION_POLICY
from edxbackup.retention import retention_from_conf
from edxbackup.retention import table_info


@click.argument("containers", required=False, nargs=-1)
@click.command(name="info")
def info(containers):
    click.echo("under construction")
