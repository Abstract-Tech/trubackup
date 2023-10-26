from trubackup.config import TrubackupConfig
from trubackup.mongo import dump_mongo_db
from trubackup.mysql import dump_mysql_db
from trubackup.postgresql import dump_postgresql_db
from trubackup.options import backup_time_option
from trubackup.options import config_path_option
from trubackup.s3 import dump_s3_bucket
from trubackup.localfs import dump_local_fs
from trubackup.utils import log_failure
from trubackup.utils import log_success

import click
import uuid


@config_path_option
@backup_time_option
@click.command(name="backup")
def perform_backup(config, time) -> None:
    """
    Perform backup
    """
    config = TrubackupConfig.parse_file(config)
    backup_id = str(uuid.uuid1())
    backup_success = True

    log_success(f"trubackup backup started: {backup_id}")

    for mongo_config in config.mongo:
        if dump_mongo_db(mongo_config, config.prefix, backup_id, time):
            log_success(f"trubackup backed up mongo database: {mongo_config.database}")
        else:
            backup_success = False
            log_failure(
                f"trubackup failed to backup mongo database: {mongo_config.database}"
            )

    for mysql_config in config.mysql:
        if dump_mysql_db(mysql_config, config.prefix, backup_id, time):
            log_success(f"trubackup backed up mysql database: {mysql_config.database}")
        else:
            backup_success = False
            log_failure(
                f"trubackup failed to backup mysql database: {mysql_config.database}"
            )

    for postgresql_config in config.postgresql:
        if dump_postgresql_db(postgresql_config, config.prefix, backup_id, time):
            log_success(
                f"trubackup backed up postgresql database: {postgresql_config.database}"
            )
        else:
            backup_success = False
            log_failure(
                f"trubackup failed to backup postgresql database: {postgresql_config.database}"
            )

    for s3_config in config.s3:
        if dump_s3_bucket(s3_config, config.prefix, backup_id, time):
            log_success(f"trubackup backed up S3 bucket: {s3_config.bucket}")
        else:
            backup_success = False
            log_failure(f"trubackup failed to backup S3 bucket: {s3_config.bucket}")

    for localfs_config in config.localfs:
        if dump_local_fs(localfs_config, backup_id, time):
            log_success(f"trubackup backed up local path: {localfs_config.path}")
        else:
            backup_success = False
            log_failure(f"trubackup failed to backup local path: {localfs_config.path}")

    if backup_success:
        log_success(f"trubackup backup finished\n{backup_id}")
    else:
        log_failure(f"trubackup backup finished with errors\n{backup_id}")
        exit(1)
