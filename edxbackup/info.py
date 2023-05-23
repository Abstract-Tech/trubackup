from edxbackup.restic.snapshot import list_snapshot_groups
from edxbackup.restic.snapshot import list_snapshots

import click


@click.command(name="list")
def list_groups() -> None:
    """
    Show list of snapshot groups
    """
    snapshot_groups = list_snapshot_groups()

    for group_id, snapshots in snapshot_groups.items():
        echo_items = [
            group_id,
            snapshots[0].time,
        ]
        click.echo("\t".join(echo_items))


@click.argument("backup_id", nargs=1)
@click.command(name="show")
def show_group(backup_id) -> None:
    """
    Show snapshots under specific group
    """
    snapshots = list_snapshots(backup_id)

    for snapshot in snapshots:
        tags_string = ",".join(snapshot.tags)
        echo_items = [snapshot.short_id, tags_string]
        click.echo("\t".join(echo_items))
