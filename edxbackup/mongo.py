"""
MongoDB dump and restore functions.

mongodump/mongorestore is a runtime dependency
"""
from datetime import datetime
from edxbackup.context import MongoTarget
from edxbackup.restic.backup import backup_stdin
from edxbackup.restic.restore import restore_stream
from pydantic import BaseModel


class MongoConfig(BaseModel):
    host: str
    port: int
    user: str | None
    password: str | None
    database: str

    def to_backup_options(self) -> list[str]:
        """
        Return a Popen args list to be used with mongodump CLI tool
        """
        options = [
            "--archive",
            f"--host={self.host}:{self.port}",
            f"--db={self.database}",
        ]

        has_auth = self.user is not None and self.password is not None
        if has_auth:
            options += [
                f"--username={self.user}",
                f"--password={self.password}",
                "--authenticationDatabase=admin",
            ]

        return options

    def to_restore_options(self) -> list[str]:
        """
        Return a Popen args list to be used with mongorestore CLI tool
        """
        options = [
            "--archive",
            "--drop",
            f"--host={self.host}:{self.port}",
        ]

        has_auth = self.user is not None and self.password is not None
        if has_auth:
            options += [
                f"--username={self.user}",
                f"--password={self.password}",
                "--authenticationDatabase=admin",
            ]

        return options


def dump_mongo_db(
    mongo_info: MongoConfig, prefix: str, backup_id: str, backup_time: datetime
) -> bool:
    backup_args = ["mongodump", "--archive"] + mongo_info.to_backup_options()

    return backup_stdin(
        backup_args,
        f"{prefix}_mongo_{mongo_info.database}",
        backup_id,
        ["mongo", f"mongo-db:{mongo_info.database}"],
        backup_time,
    )


def restore_mongo_db(mongo_info: MongoConfig, target: MongoTarget) -> bool:
    restore_args = ["mongorestore"] + mongo_info.to_restore_options()

    return restore_stream(
        restore_args,
        target.id,
        target.path,
    )
