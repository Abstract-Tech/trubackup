from edxbackup.config import EdxbackupConfig
from edxbackup.context import build_context
from edxbackup.context import get_mongo_target
from edxbackup.context import get_mysql_target
from edxbackup.context import get_postgresql_target
from edxbackup.context import get_s3_target
from edxbackup.mongo import restore_mongo_db
from edxbackup.mysql import restore_mysql_db
from edxbackup.options import config_path_option
from edxbackup.postgresql import restore_postgresql_db
from edxbackup.restic.snapshot import list_snapshots
from edxbackup.s3 import restore_s3_bucket
from edxbackup.utils import log_failure
from edxbackup.utils import log_success

import click


@config_path_option
@click.argument("backup_id", nargs=1)
@click.command(name="restore")
def perform_restore(config, backup_id) -> None:
    """
    Perform restore
    """
    config = EdxbackupConfig.parse_file(config)

    snapshots = list_snapshots(backup_id)
    backup_context = build_context(snapshots)

    log_success(f"edxbackup restore started: {backup_id}")
    for mongo_config in config.mongo:
        mongo_db = mongo_config.database
        mongo_target = get_mongo_target(backup_context, mongo_db)
        if mongo_target is not None:
            if restore_mongo_db(mongo_config, mongo_target):
                log_success(f"edxbackup restored mongo database: {mongo_db}")
            else:
                log_failure(f"edxbackup failed to restore mongo database: {mongo_db}")
        else:
            log_failure(
                f"edxbackup failed to restore mongo database (no snapshot): {mongo_db}"
            )

    for mysql_config in config.mysql:
        mysql_db = mysql_config.database
        mysql_target = get_mysql_target(backup_context, mysql_db)
        if mysql_target is not None:
            if restore_mysql_db(mysql_config, mysql_target):
                log_success(f"edxbackup restored mysql database: {mysql_db}")
            else:
                log_failure(f"edxbackup failed to restore mysql database: {mysql_db}")
        else:
            log_failure(
                f"edxbackup failed to restore mysql database (no snapshot): {mysql_db}"
            )

    for postgresql_config in config.postgresql:
        postgresql_db = postgresql_config.database
        postgresql_target = get_postgresql_target(backup_context, postgresql_db)
        if postgresql_target is not None:
            if restore_postgresql_db(postgresql_config, postgresql_target):
                log_success(f"edxbackup restored postgresql database: {postgresql_db}")
            else:
                log_failure(
                    f"edxbackup failed to restore postgresql database: {postgresql_db}"
                )
        else:
            log_failure(
                f"edxbackup failed to restore postgresql database (no snapshot): {postgresql_db}"
            )

    for s3_config in config.s3:
        s3_bucket = s3_config.bucket
        s3_target = get_s3_target(backup_context, s3_config.bucket)
        if s3_target is not None:
            if restore_s3_bucket(s3_config, s3_target):
                log_success(f"edxbackup restored S3 bucket: {s3_bucket}")
            else:
                log_success(f"edxbackup failed to restore S3 bucket: {s3_bucket}")
        else:
            log_failure(
                f"edxbackup failed to restore S3 bucket (no snapshot): {s3_bucket}"
            )

    log_success(f"edxbackup restore finished\n{backup_id}")
