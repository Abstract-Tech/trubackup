"""
PostgreSQL dump and restore functions.
"""
import os

from datetime import datetime
from edxbackup.context import MysqlTarget, PostgresqlTarget
from edxbackup.restic.backup import backup_stdin
from edxbackup.restic.restore import restore_stream
from pydantic import BaseModel


class PostgresqlConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    database: str

    def to_backup_options(self) -> list[str]:
        """
        Return a Popen args list to be used with pd_dumper CLI tool
        """
        return [
            f"--host={self.host}",
            f"--port={self.port}",
            f"--username={self.user}",
            "--format=c",
            f"{self.database}",
        ]

    def to_restore_options(self) -> list[str]:
        """
        Return a Popen args list to be used with pg_restore CLI tools
        """
        return [
            "--clean",
            "--create",
            f"--host={self.host}",
            f"--port={self.port}",
            f"--username={self.user}",
            "--dbname=postgres",
        ]


def dump_postgresql_db(
    postgresql_info: PostgresqlConfig,
    prefix: str,
    backup_id: str,
    backup_time: datetime,
) -> bool:
    backup_args = [
        "pg_dump",
    ] + postgresql_info.to_backup_options()

    os.environ["PGPASSWORD"] = postgresql_info.password

    try:
        return backup_stdin(
            backup_args,
            f"{prefix}_postgresql_{postgresql_info.database}",
            backup_id,
            ["postgresql", f"postgresql-db:{postgresql_info.database}"],
            backup_time,
        )
    finally:
        del os.environ["PGPASSWORD"]


def restore_postgresql_db(
    postgresql_info: PostgresqlConfig, target: PostgresqlTarget
) -> bool:
    restore_args = [
        "pg_restore",
    ] + postgresql_info.to_restore_options()

    os.environ["PGPASSWORD"] = postgresql_info.password

    try:
        return restore_stream(
            restore_args,
            target.id,
            target.path,
        )
    finally:
        del os.environ["PGPASSWORD"]
