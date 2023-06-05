from datetime import datetime
from subprocess import PIPE
from subprocess import Popen


def backup_stdin(
    backup_args: list[str],
    filename: str,
    hostname: str,
    tags: list[str],
    date: datetime | None = None,
) -> bool:
    str_date = "now"
    if date is not None:
        str_date = date.strftime("%Y-%m-%d %H:%M:%S")

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
