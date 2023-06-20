from collections.abc import Iterator
from edxbackup.restic.snapshot import ResticSnapshot
from pydantic import BaseModel


class MysqlTarget(BaseModel):
    id: str
    db: str
    path: str


class PostgresqlTarget(BaseModel):
    id: str
    db: str
    path: str


class MongoTarget(BaseModel):
    id: str
    db: str
    path: str


class S3Target(BaseModel):
    id: str
    bucket: str
    path: str


class BackupContext(BaseModel):
    """
    A class to process and store restic snapshot ids categorized by different
    backup targets
    """

    mysql: list[MysqlTarget]
    postgresql: list[PostgresqlTarget]
    mongo: list[MongoTarget]
    s3: list[S3Target]


def build_context(snapshots: list[ResticSnapshot]) -> BackupContext:
    def tags_to_database(engine, tags) -> str:
        db_tag = next(tag for tag in tags if tag.startswith(f"{engine}-db:"))
        return db_tag.split(":")[1]

    def extract_mysql(snapshots: list[ResticSnapshot]) -> Iterator[MysqlTarget]:
        for snapshot in snapshots:
            if "mysql" in snapshot.tags:
                yield MysqlTarget(
                    id=snapshot.id,
                    db=tags_to_database("mysql", snapshot.tags),
                    path=snapshot.paths[0],
                )

    def extract_postgresql(
        snapshots: list[ResticSnapshot],
    ) -> Iterator[PostgresqlTarget]:
        for snapshot in snapshots:
            if "postgresql" in snapshot.tags:
                yield PostgresqlTarget(
                    id=snapshot.id,
                    db=tags_to_database("postgresql", snapshot.tags),
                    path=snapshot.paths[0],
                )

    def extract_mongo(snapshots: list[ResticSnapshot]) -> Iterator[MongoTarget]:
        for snapshot in snapshots:
            if "mongo" in snapshot.tags:
                yield MongoTarget(
                    id=snapshot.id,
                    db=tags_to_database("mongo", snapshot.tags),
                    path=snapshot.paths[0],
                )

    def extract_s3(snapshots: list[ResticSnapshot]) -> Iterator[S3Target]:
        for snapshot in snapshots:
            if "s3" in snapshot.tags:
                yield S3Target(
                    id=snapshot.id,
                    bucket=tags_to_database("s3", snapshot.tags),
                    path=snapshot.paths[0],
                )

    return BackupContext(
        mysql=list(extract_mysql(snapshots)),
        postgresql=list(extract_postgresql(snapshots)),
        mongo=list(extract_mongo(snapshots)),
        s3=list(extract_s3(snapshots)),
    )


def get_mongo_target(context: BackupContext, database: str) -> MongoTarget | None:
    """
    Get MongoTarget with matching db name from backup context
    """
    for mongo_target in context.mongo:
        if mongo_target.db == database:
            return mongo_target

    return None


def get_mysql_target(context: BackupContext, database: str) -> MysqlTarget | None:
    """
    Get MysqlTarget with matching db name from backup context
    """
    for mysql_target in context.mysql:
        if mysql_target.db == database:
            return mysql_target

    return None


def get_postgresql_target(
    context: BackupContext, database: str
) -> PostgresqlTarget | None:
    """
    Get PostgresqlTarget with matching db name from backup context
    """
    for postgresql_target in context.postgresql:
        if postgresql_target.db == database:
            return postgresql_target

    return None


def get_s3_target(context: BackupContext, bucket: str) -> S3Target | None:
    """
    Get S3Target with matching bucket name from backup context
    """
    for s3_target in context.s3:
        if s3_target.bucket == bucket:
            return s3_target

    return None
