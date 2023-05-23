from click import DateTime
from datetime import datetime

import click


backup_time_option = click.option(
    "--time",
    type=DateTime(),
    envvar="EDXBACKUP_BACKUP_TIME",
    default=datetime.now(),
    help="Override backup time",
)

config_path_option = click.option(
    "--config",
    "-c",
    envvar="EDXBACKUP_CONFIG_PATH",
    default="/etc/edxbackup.json",
    help="Path to JSON file containing info about databases to dump",
)
