from copy import deepcopy
from datetime import datetime
from datetime import timedelta
from pathlib import Path
from uuid import uuid4
import json

from typing import List
from typing import Tuple

from click.testing import CliRunner
from swiftclient.service import SwiftUploadObject


BASE_CONFIG = json.loads((Path(__file__).parent / "dump_conf.json").read_text())


def test_remove_old_local(tmp_path):
    from edxbackup.bookkeeping import remove_old

    dumps_path = tmp_path / "dumps"
    dumps_path.mkdir()
    create_dump_dirs(
        dumps_path,
        [
            (2017, 2, 1, 12, 0),
            (2017, 1, 31, 12, 0),
            (2017, 1, 31, 10, 0),
            (2017, 1, 31, 9, 0),
            (2017, 1, 31, 8, 0),
            (2017, 1, 30, 12, 0),
            (2017, 1, 20, 12, 0),
            (2017, 1, 17, 12, 0),
            (2017, 1, 16, 12, 0),
        ],
    )
    a_file = dumps_path / "a_file"
    a_file.write_text("something")
    (tmp_path / "config").mkdir()

    config_file = tmp_path / "config" / "config.json"
    config_file.write_text("{}")
    runner = CliRunner()
    result = runner.invoke(
        remove_old,
        ["--dump-location", str(dumps_path), "--dbconfig-path", str(config_file)],
    )
    assert result.exit_code == 0, result.exception
    # Files that do not parse as iso datetimes should have been left untouched
    assert a_file.read_text() == "something"

    # The default retention policy should have been added
    assert (dumps_path / "retention_policy.json").is_file()


def test_remove_old_swift(tmp_path):
    from edxbackup.bookkeeping import remove_old_remote_swift

    container = str(uuid4())
    to_upload = []
    for i in range(30):
        dt = datetime.utcnow() - timedelta(days=i)
        path = "/".join([dt.isoformat(), "dummy"])
        to_upload.append(SwiftUploadObject(None, object_name=f"{path}"))
    with getSwiftService() as swift:
        problems = [
            el for el in swift.upload(container, to_upload) if not el["success"]
        ]
    if problems:
        print("There were problems uploading the dump via swift")
        print(problems)
        raise ValueError(str(problems))
    remove_old_remote_swift(get_config_for(tmp_path, container))
    timestamps = []
    with getSwiftService() as swift:
        for res in swift.list(container, options=dict(prefix="", delimiter="/")):
            timestamps += [el["subdir"] for el in res["listing"] if "subdir" in el]
    assert 10 < len(timestamps) < 20


def get_config_for(tmp_path, container):
    """Use dump_conf.json as a base, change its `swift`/`container` value
    to the given one, save to a temp file and and return its path.
    """
    config = deepcopy(BASE_CONFIG)
    config["swift"]["container"] = container
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config))
    return str(config_file)


def getSwiftService():
    from edxbackup.swift import getSwiftService

    return getSwiftService(BASE_CONFIG)


def create_dump_dirs(path: Path, dts: List[Tuple[int]]):
    """Given a path and a list of ints representing datetime objects,
    create directories with names in ISO format.
    """
    for dt in dts:
        (path / datetime(*dt).isoformat()).mkdir()  # type: ignore
