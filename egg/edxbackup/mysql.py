"""
MySQL dump and restore functions.

https://github.com/mydumper/mydumper is a runtime requirement
"""
import os

import click

from edxbackup.config import MysqlConfig


def dump_mysql_db(mysql_info: MysqlConfig, output_dir: str):
    dump_path = os.path.join(output_dir, f"mysql_dump_{mysql_info.dbname}")

    cmd = f"mydumper --compress {mysql_info.to_cli_options()} -o {dump_path}"
    click.echo(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo(f"Error dumping mysql db {mysql_info.dbname}")


def restore_mysql_db(mysql_info: MysqlConfig, output_dir: str):
    dump_path = os.path.join(output_dir, f"mysql_dump_{mysql_info.dbname}")

    cmd = f"myloader {mysql_info.to_cli_options()} --overwrite-tables --directory {dump_path}"
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo("Error restoring mysql")
        click.get_current_context().fail()
