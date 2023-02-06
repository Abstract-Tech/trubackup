"""
MongoDB dump and restore functions.

mongodump/mongorestore is a runtime dependency
"""
import os

import click

from edxbackup.config import MongoConfig


def dump_mongo_db(mongo_info: MongoConfig, output_dir: str):
    dump_path = os.path.join(output_dir, f"mongodb_dump_{mongo_info.dbname}.tar.gz")

    cmd = f"mongodump {mongo_info.to_cli_options()} --gzip --archive={dump_path}"
    click.echo(f"Running:\n {cmd}")
    if os.system(cmd) != 0:
        click.echo(f"Error dumping mongo db {mysql_info.dbname}")


def restore_mongo_db(mongo_info: MongoConfig, output_dir: str):
    dump_path = os.path.join(output_dir, f"mongodb_dump_{mongo_info.dbname}.tar.gz")

    cmd = f"mongorestore {mongo_info.to_cli_options()} --gzip --archive={dump_path}"
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo("Error restoring mongo")
        click.get_current_context().fail()
