from datetime import datetime
from pathlib import Path

from click.testing import CliRunner


def test_remove_old(tmp_path):
    from edxbackup.bookkeeping import remove_old

    dumps_path = tmp_path / "dumps"
    dumps_path.mkdir()
    (tmp_path / "config").mkdir()

    config_file = tmp_path / "config" / "config.json"
    config_file.write_text("{}")
    runner = CliRunner()
    runner.invoke(
        remove_old,
        ["--dump-location", str(dumps_path), "--dbconfig-path", str(config_file)],
    )
