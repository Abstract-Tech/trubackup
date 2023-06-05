from subprocess import PIPE
from subprocess import Popen


def restore_stream(restore_args: list[str], snapshot_id: str, path: str) -> bool:
    download_args = [
        "restic",
        "dump",
        snapshot_id,
        path,
    ]

    download_process = Popen(download_args, stdout=PIPE)
    restore_process = Popen(restore_args, stdin=download_process.stdout)

    download_process.stdout.close()  # type: ignore
    restore_process.communicate()
    download_process.wait()
    restore_process.wait()

    return (download_process.returncode + restore_process.returncode) == 0
