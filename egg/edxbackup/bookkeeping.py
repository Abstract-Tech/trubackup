from datetime import datetime
from pathlib import Path
import io
import json
import shutil
import tempfile

import click
import pendulum
from pendulum.exceptions import ParserError

from edxbackup.config import EdxbackupConfig
from edxbackup.options import dbconfig_path_option
from edxbackup.options import dump_location_option
from edxbackup.retention import retention_from_conf
from edxbackup.retention import to_delete


DEFAULT_RETENTION_POLICY = (({"days": 1}, 8), ({"days": 7}, 5), ({"days": 28}, 7))


@dump_location_option(type=click.Path())
@dbconfig_path_option
@click.option("--local/--no-local", default=True)
@click.command(name="remove_old")
def remove_old(dump_location, dbconfig_path, local):
    if local:
        remove_old_local(dump_location)


def remove_old_local(dump_location):
    dump_path = Path(dump_location)
    retention_policy = load_retention_policy(dump_path)
    if retention_policy is None:
        retention_policy = create_default_retention_policy(dump_path)
    elements = []
    for dirpath in dump_path.iterdir():
        if dirpath.is_dir():
            pendulum_dt = pendulum.parse(dirpath.name).timestamp()
            dt = datetime.fromtimestamp(pendulum_dt)
            elements.append((dt, dirpath))
    elements_to_delete = to_delete(retention_policy, elements)
    for _, path in elements_to_delete:
        shutil.rmtree(path)


def load_retention_policy(dump_path):
    rp_location = dump_path / "retention_policy.json"
    if rp_location.is_file():
        return retention_from_conf(json.load(rp_location.open()))


def create_default_retention_policy(dump_path):
    rp_location = dump_path / "retention_policy.json"
    json.dump(DEFAULT_RETENTION_POLICY, rp_location.open("w"))
    return retention_from_conf(DEFAULT_RETENTION_POLICY)
