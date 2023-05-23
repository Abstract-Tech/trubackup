from datetime import datetime
from subprocess import PIPE
from subprocess import Popen
import tarfile

from minio import Minio


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


def backup_s3(
    s3_config,
    filename: str,
    hostname: str,
    tags: list[str],
    date: datetime | None = None,
) -> bool:
    str_date = "now"
    if date is not None:
        str_date = date.strftime("%Y-%m-%d %H:%M:%S")

    s3_client = Minio(
        s3_config.host,
        s3_config.access_key,
        s3_config.secret_key,
        secure=s3_config.https,
    )

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

    process = Popen(upload_args, stdin=PIPE)

    objects = s3_client.list_objects(s3_config.bucket, recursive=True)
    with tarfile.open(mode="w|", fileobj=process.stdin) as tar:
        for obj in objects:
            if not obj.is_dir:
                obj_key = obj.object_name
                obj_stream = s3_client.get_object(s3_config.bucket, obj_key)

                tarinfo = tarfile.TarInfo(name=obj_key)
                tarinfo.size = obj.size

                tar.addfile(tarinfo, fileobj=obj_stream)

    process.stdin.close()  # type: ignore
    process.wait()

    return process.returncode == 0
