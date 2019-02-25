import os
import datetime

import click

from edxbackup import options


edx_config = click.option(
    "--edx-config",
    envvar="EDX_CONFIG",
    default='-',
    help="Path to lms.auth.json or cms.auth.json",
)


@edx_config
@click.command(name="edx_dump")
def dump(edx_config):
    """Dump Mysql and MongoDB databases relative to the given edX instance"""
    config = click.open_file(edx_config).read()


@edx_config
@click.command(name="edx_restore")
def restore(edx_config):
    """Restore Mysql and MongoDB databases relative to the given edX instance"""
