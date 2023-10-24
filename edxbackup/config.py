from edxbackup.mongo import MongoConfig
from edxbackup.mysql import MysqlConfig
from edxbackup.postgresql import PostgresqlConfig
from edxbackup.s3 import S3Config
from edxbackup.localfs import LocalFSConfig
from pydantic import BaseModel


class EdxbackupConfig(BaseModel):
    mysql: list[MysqlConfig]
    postgresql: list[PostgresqlConfig]
    mongo: list[MongoConfig]
    s3: list[S3Config]
    localfs: list[LocalFSConfig]
    prefix: str
