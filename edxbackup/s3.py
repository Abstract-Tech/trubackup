from datetime import datetime
from edxbackup.context import S3Target
from edxbackup.restic.backup import backup_stdin
from edxbackup.restic.restore import restore_stream
from pydantic import BaseModel


class S3Config(BaseModel):
    host: str
    access_key: str
    secret_key: str
    https: bool
    bucket: str

    def to_backup_options(self) -> list[str]:
        """
        Return a Popen args list to be used with mydumper CLI tool
        """
        protocol = "https" if self.https else "http"
        return [
            f"--endpoint={self.host}",
            f"--access-key={self.access_key}",
            f"--secret-key={self.secret_key}",
            f"--protocol={protocol}",
            self.bucket,
        ]

    def to_restore_options(self) -> list[str]:
        """
        Return a Popen args list to be used with mydumper CLI tool
        """
        protocol = "https" if self.https else "http"
        return [
            f"--endpoint={self.host}",
            f"--access-key={self.access_key}",
            f"--secret-key={self.secret_key}",
            f"--protocol={protocol}",
            self.bucket,
        ]


def dump_s3_bucket(
    s3_config: S3Config, prefix: str, backup_id: str, backup_time: datetime
) -> bool:
    backup_args = [
        "s3ball",
        "download",
    ] + s3_config.to_backup_options()

    return backup_stdin(
        backup_args,
        f"{prefix}_s3",
        backup_id,
        ["s3", f"s3-db:{s3_config.bucket}"],
        backup_time,
    )


def restore_s3_bucket(s3_config: S3Config, target: S3Target) -> bool:
    restore_args = [
        "s3ball",
        "upload",
    ] + s3_config.to_backup_options()

    return restore_stream(restore_args, target.id, target.path)
