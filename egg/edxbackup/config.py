from typing import Dict, List, Optional

from pydantic import BaseModel


class MysqlConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    dbname: str

    def to_cli_options(self, censored=False):
        """
        Return a string to be used with mydumper/myloader

        Args:
            censored: does not render password if set to true
        """
        return (
            f"--host {self.host} "
            f"--port {self.port} "
            f"--user {self.user} "
            f"--password {self.password if not censored else '*****'} "
            f"--database {self.dbname} "
        )


class MongoConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    dbname: str

    def to_cli_options(self, censored=False):
        """
        Return a string to be used with mongodump/mongorestore

        Args:
            censored: does not render password if set to true
        """
        return (
            f"--host={self.host}:{self.port} "
            f"--username={self.user} "
            f"--password={self.password if not censored else '*****'} "
            f"--db={self.dbname} "
            f"--authenticationDatabase=admin"
        )


class S3Config(BaseModel):
    host: str
    access_key: str
    secret_key: str
    https: bool


class UploadConfig(BaseModel):
    remote_name: str
    destination: str


class EdxbackupConfig(BaseModel):
    mysql: List[MysqlConfig]
    mongo: List[MongoConfig]
    s3: Optional[S3Config]
    upload: Optional[UploadConfig]
