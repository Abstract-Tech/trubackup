from trubackup.mongo import MongoConfig
from trubackup.mysql import MysqlConfig
from trubackup.postgresql import PostgresqlConfig
from trubackup.s3 import S3Config
from trubackup.localfs import LocalFSConfig
from pydantic import BaseModel


class TrubackupConfig(BaseModel):
    mysql: list[MysqlConfig]
    postgresql: list[PostgresqlConfig]
    mongo: list[MongoConfig]
    s3: list[S3Config]
    localfs: list[LocalFSConfig]
    prefix: str
