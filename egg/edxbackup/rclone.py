import subprocess
import shutil

import dateutil

from pydantic import BaseModel, validator


class RcloneItem(BaseModel):
    Path: str
    Name: str
    Size: int
    MimeType: str
    ModTime: str
    IsDir: bool
    IsBucket: bool

    @validator("ModTime")
    def validate_modtime(cls, v) -> str:
        return dateutil.parser.isoparse(v)


def rclone_exists() -> bool:
    return shutil.which("rclone") is not None


def copy(source: str, remote: str, destination: str):
    """
    'rclone copy' wrapper
    """
    merged_destination = f"{remote}:{destination}"

    rclone_command = [
        "rclone", "copy", "--create-empty-src-dirs", source, merged_destination
    ]

    print(' '.join(rclone_command))

    cp = subprocess.run(
        rclone_command,
        check=False,
    )

    if cp.returncode != 0:
        raise RuntimeError(f"Failed to upload f{source} to f{merged_destination}")
