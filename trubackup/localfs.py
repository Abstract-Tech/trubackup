from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, field_validator

from trubackup.context import LocalFSTarget
from trubackup.restic.backup import backup_fs
from trubackup.restic.restore import restore_fs


class LocalFSConfig(BaseModel):
    path: str

    @field_validator("path")
    @classmethod
    def path_must_exist(cls, str_path: str):
        if not Path(str_path).exists():
            raise ValueError("Path %s does not exist in filesystem", str_path)
        return str_path


def dump_local_fs(
    local_info: LocalFSConfig,
    backup_id: str,
    backup_time: datetime,
) -> bool:
    local_path = Path(local_info.path)
    return backup_fs(
        local_path,
        backup_id,
        ["localfs", f"localfs-path:{local_info.path}"],
        backup_time,
    )


def restore_local_fs(local_info: LocalFSConfig, target: LocalFSTarget) -> bool:
    return restore_fs(Path(local_info.path), target.id)
