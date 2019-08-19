from datetime import datetime

from swiftclient.service import SwiftService
import click

from edxbackup.bookkeeping import DEFAULT_RETENTION_POLICY
from edxbackup.retention import retention_from_conf
from edxbackup.retention import table_info
from edxbackup.swift import get_timestamps


@click.argument("containers", required=False, nargs=-1)
@click.command(name="info")
def info(containers):
    now = datetime.utcnow()
    with SwiftService() as swift:
        if not containers:
            containers = get_containers(swift)
        for container in containers:
            click.echo(f"Container {container}")
            timestamps = get_timestamps(container, swift)
            click.echo(
                table_info(
                    timestamps, now, retention_from_conf(DEFAULT_RETENTION_POLICY)
                )
            )


def get_containers(swift):
    return [el["name"] for res in swift.list() for el in res["listing"]]
