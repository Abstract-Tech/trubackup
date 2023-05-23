"""
MySQL dump and restore functions.

https://github.com/mydumper/mydumper is a runtime requirement
"""
from datetime import datetime
from edxbackup.context import MysqlTarget
from edxbackup.restic.backup import backup_stdin
from edxbackup.restic.restore import restore_stream
from pydantic import BaseModel


class MysqlConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str

    def to_backup_options(self) -> list[str]:
        """
        Return a Popen args list to be used with mydumper CLI tool
        """
        return [
            "--stream",
            f"--host={self.host}",
            f"--port={self.port}",
            f"--user={self.user}",
            f"--password={self.password}",
            f"--database={self.database}",
        ]

    def to_restore_options(self) -> list[str]:
        """
        Return a Popen args list to be used with myloader CLI tools
        """
        return [
            "--stream",
            "--overwrite-tables",
            f"--host={self.host}",
            f"--port={self.port}",
            f"--user={self.user}",
            f"--password={self.password}",
            f"--database={self.database}",
        ]


def dump_mysql_db(
    mysql_info: MysqlConfig, prefix: str, backup_id: str, backup_time: datetime
) -> bool:
    backup_args = [
        "mydumper",
    ] + mysql_info.to_backup_options()

    return backup_stdin(
        backup_args,
        f"{prefix}_mysql_{mysql_info.database}",
        backup_id,
        ["mysql", f"mysql-db:{mysql_info.database}"],
        backup_time,
    )


def restore_mysql_db(mysql_info: MysqlConfig, target: MysqlTarget) -> bool:
    restore_args = [
        "myloader",
    ] + mysql_info.to_restore_options()

    return restore_stream(
        restore_args,
        target.id,
        target.path,
    )
