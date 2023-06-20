from edxbackup.config import EdxbackupConfig
from edxbackup.mongo import dump_mongo_db
from edxbackup.mysql import dump_mysql_db
from edxbackup.postgresql import dump_postgresql_db
from edxbackup.options import backup_time_option
from edxbackup.options import config_path_option
from edxbackup.s3 import dump_s3_bucket
from edxbackup.utils import log_failure
from edxbackup.utils import log_success

import click
import uuid


@config_path_option
@backup_time_option
@click.command(name="backup")
def perform_backup(config, time) -> None:
    """
    Perform backup
    """
    config = EdxbackupConfig.parse_file(config)
    backup_id = str(uuid.uuid1())

    log_success(f"edxbackup backup started: {backup_id}")

    for mongo_config in config.mongo:
        if dump_mongo_db(mongo_config, config.prefix, backup_id, time):
            log_success(f"edxbackup backed up mongo database: {mongo_config.database}")
        else:
            log_failure(
                f"edxbackup failed to backup mongo database: {mongo_config.database}"
            )

    for mysql_config in config.mysql:
        if dump_mysql_db(mysql_config, config.prefix, backup_id, time):
            log_success(f"edxbackup backed up mysql database: {mysql_config.database}")
        else:
            log_failure(
                f"edxbackup failed to backup mysql database: {mysql_config.database}"
            )

    for postgresql_config in config.postgresql:
        if dump_postgresql_db(postgresql_config, config.prefix, backup_id, time):
            log_success(
                f"edxbackup backed up postgresql database: {postgresql_config.database}"
            )
        else:
            log_failure(
                f"edxbackup failed to backup postgresql database: {postgresql_config.database}"
            )

    for s3_config in config.s3:
        if dump_s3_bucket(s3_config, config.prefix, backup_id, time):
            log_success(f"edxbackup backed up S3 bucket: {s3_config.bucket}")
        else:
            log_failure(f"edxbackup failed to backup S3 bucket: {s3_config.bucket}")

    log_success(f"edxbackup backup finished\n{backup_id}")
