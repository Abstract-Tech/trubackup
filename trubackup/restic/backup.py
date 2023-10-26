from datetime import datetime
from pathlib import Path
from subprocess import PIPE
from subprocess import Popen


def date2str(date: datetime | None) -> str:
    """
    Convert datetime to format supported by restic

    Returns "now" if date is None
    """
    str_date = "now"
    if date is not None:
        str_date = date.strftime("%Y-%m-%d %H:%M:%S")

    return str_date


def backup_stdin(
    backup_args: list[str],
    filename: str,
    hostname: str,
    tags: list[str],
    date: datetime | None = None,
) -> bool:
    str_date = date2str(date)
    upload_args = [
        "restic",
        "backup",
        "--stdin",
        "--stdin-filename",
        filename,
        "--host",
        hostname,
        "--tag",
        ",".join(tags),
        "--time",
        str_date,
    ]

    backup_process = Popen(backup_args, stdout=PIPE)
    upload_process = Popen(upload_args, stdin=backup_process.stdout)

    backup_process.stdout.close()  # type: ignore
    upload_process.communicate()
    backup_process.wait()
    upload_process.wait()

    return (backup_process.returncode + upload_process.returncode) == 0


def backup_fs(
    path: Path,
    hostname: str,
    tags: list[str],
    date: datetime | None = None,
):
    str_date = date2str(date)
    upload_args = [
        "restic",
        "backup",
        str(path),
        "--host",
        hostname,
        "--tag",
        ",".join(tags),
        "--time",
        str_date,
    ]

    upload_process = Popen(upload_args, stdout=PIPE)
    upload_process.wait()

    return upload_process.returncode == 0
