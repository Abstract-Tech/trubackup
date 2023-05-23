from subprocess import PIPE
from subprocess import Popen

from minio import Minio
import tarfile


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


def restore_s3(s3_config, snapshot_id: str, path: str) -> bool:
    s3_client = Minio(
        s3_config.host,
        s3_config.access_key,
        s3_config.secret_key,
        secure=s3_config.https,
    )

    download_args = [
        "restic",
        "dump",
        snapshot_id,
        path,
    ]

    download_process = Popen(download_args, stdout=PIPE)

    with tarfile.open(mode="r|", fileobj=download_process.stdout) as tar:
        for tarinfo in tar:
            if tarinfo.isfile():
                object_key = tarinfo.name

                ex_reader = tar.extractfile(tarinfo)
                s3_client.put_object(
                    s3_config.bucket, object_key, ex_reader, tarinfo.size
                )

    download_process.wait()

    return download_process.returncode == 0
