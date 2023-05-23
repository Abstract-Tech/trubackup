from datetime import datetime
from edxbackup.context import S3Target
from edxbackup.restic.backup import backup_s3
from edxbackup.restic.restore import restore_s3
from pydantic import BaseModel


class S3Config(BaseModel):
    host: str
    access_key: str
    secret_key: str
    https: bool
    bucket: str


def dump_s3_bucket(
    s3_config: S3Config, prefix: str, backup_id: str, backup_time: datetime
) -> bool:
    """
    Dump every object at specified S3 bucket into a directory
    """
    return backup_s3(
        s3_config,
        f"{prefix}_s3",
        backup_id,
        ["s3", f"s3-db:{s3_config.bucket}"],
        backup_time,
    )


def restore_s3_bucket(s3_config: S3Config, target: S3Target) -> bool:
    """
    Upload every file from .tar archvie into S3 bucket
    """
    # FIXME: Handle failure situations
    return restore_s3(s3_config, target.id, target.path)
