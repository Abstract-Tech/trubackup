from datetime import datetime
from pathlib import Path

from typing import List
from typing import Tuple

from click.testing import CliRunner


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
    from edxbackup.bookkeeping import remove_old

    config_file = Path(__file__).parent / "dump_conf.json"
    runner = CliRunner()
    result = runner.invoke(
        remove_old,
        ["--dbconfig-path", str(config_file), "--no-local", "--remote-swift"],
    )
    assert result.exit_code == 0, result.exception


def create_dump_dirs(path: Path, dts: List[Tuple[int]]):
    """Given a path and a list of ints representing datetime objects,
    create directories with names in ISO format.
    """
    for dt in dts:
        (path / datetime(*dt).isoformat()).mkdir()  # type: ignore
