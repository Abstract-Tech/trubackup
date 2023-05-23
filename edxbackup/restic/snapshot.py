from pydantic import BaseModel
from subprocess import check_output

import json


class ResticSnapshot(BaseModel):
    """
    A model of restic snapshot as in `restic snapshots --json`
    """

    time: str
    parent: str | None
    tree: str
    paths: list[str]
    hostname: str
    username: str
    tags: list[str]
    id: str
    short_id: str


def list_snapshot_groups() -> dict[str, list[ResticSnapshot]]:
    """
    Get all snapshots grouped by hostname
    """
    list_args = ["restic", "snapshots", "--group-by", "host", "--json"]

    snaptshot_group_output = check_output(list_args)
    return {
        group["group_key"]["hostname"]: [
            ResticSnapshot(**ssnap) for ssnap in group["snapshots"]
        ]
        for group in json.loads(snaptshot_group_output)
    }


def list_snapshots(hostname: str | None = None) -> list[ResticSnapshot]:
    """
    Get all snapshots made from specific hostname
    """
    list_args = ["restic", "snapshots", "--json"]

    if hostname is not None:
        list_args += ["--host", hostname]

    snaptshots_output = check_output(list_args)
    return [ResticSnapshot(**ssnap) for ssnap in json.loads(snaptshots_output)]
