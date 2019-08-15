from datetime import datetime
from pathlib import Path
import io
import json
import shutil
import tempfile

import click
import pendulum
from pendulum.exceptions import ParserError
from swiftclient.service import SwiftUploadObject

from edxbackup.options import dbconfig_path_option
from edxbackup.options import dump_location_option
from edxbackup.retention import retention_from_conf
from edxbackup.retention import to_delete
from edxbackup.swift import getSwiftService


DEFAULT_RETENTION_POLICY = (({"days": 1}, 8), ({"days": 7}, 5), ({"days": 28}, 7))


@dump_location_option(type=click.Path())
@dbconfig_path_option
@click.option("--local/--no-local", default=True)
@click.option("--remote-swift/--no-remote-swift", default=False)
@click.command(name="remove_old")
def remove_old(dump_location, dbconfig_path, local, remote_swift):
    if local:
        remove_old_local(dump_location)
    if remote_swift:
        remove_old_remote_swift(dbconfig_path)


def remove_old_remote_swift(dbconfig_path):
    info = json.load(click.open_file(dbconfig_path))
    container = info["swift"]["container"]
    retention_policy = swift_load_retention_policy(info)
    if retention_policy is None:
        retention_policy = swift_create_default_retention_policy(info)
    elements = []
    with getSwiftService(info) as swift:
        for res in swift.list(container, options=dict(prefix="", delimiter="/")):
            elements += [el["subdir"] for el in res["listing"] if "subdir" in el]
    timestamps = []
    for element in elements:
        try:
            # `element` includes a trailing slash
            pendulum_dt = pendulum.parse(element[:-1]).timestamp()
            dt = datetime.fromtimestamp(pendulum_dt)
            timestamps.append((dt, element[:-1]))
        except ParserError:
            pass
    # We need to explicitly list all objects that we want to delete.
    # Recursively deleting a "folder" is not supported.
    objects_to_delete = []
    with getSwiftService(info) as swift:
        for _, timestamp in to_delete(retention_policy, timestamps):
            for res in swift.list(container, options=dict(prefix=timestamp)):
                objects_to_delete += [el["name"] for el in res["listing"]]
    with getSwiftService(info) as swift:
        for res in swift.delete(container, objects_to_delete):
            if not res["success"]:
                raise ValueError(res)  # TODO: more meaningful error management


def swift_load_retention_policy(info):
    container = info["swift"]["container"]
    with getSwiftService(info) as swift:
        with tempfile.TemporaryDirectory() as tmp:
            dest = str(Path(tmp) / "retention_policy.json")
            res = tuple(
                swift.download(
                    container, ["retention_policy.json"], options={"out_file": dest}
                )
            )
            if res[0]["success"]:
                return retention_from_conf(json.load(open(dest)))


def swift_create_default_retention_policy(info):
    container = info["swift"]["container"]
    with getSwiftService(info) as swift:
        objects = [
            SwiftUploadObject(
                io.BytesIO(json.dumps(DEFAULT_RETENTION_POLICY).encode()),
                object_name="retention_policy.json",
            )
        ]
        for res in swift.upload(container, objects):
            if not res["success"]:
                raise ValueError(res)

    return retention_from_conf(DEFAULT_RETENTION_POLICY)


def remove_old_local(dump_location):
    dump_path = Path(dump_location)
    retention_policy = load_retention_policy(dump_path)
    if retention_policy is None:
        retention_policy = create_default_retention_policy(dump_path)
    elements = []
    for dirpath in dump_path.iterdir():
        if dirpath.is_dir():
            elements.append(
                (datetime.strptime(dirpath.name, "%Y-%m-%dT%H:%M:%S"), dirpath)
            )
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
