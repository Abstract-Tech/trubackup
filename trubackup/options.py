from click import DateTime
from datetime import datetime

import click


backup_time_option = click.option(
    "--time",
    type=DateTime(),
    envvar="TRUBACKUP_BACKUP_TIME",
    default=datetime.now(),
    help="Override backup time",
)

config_path_option = click.option(
    "--config",
    "-c",
    envvar="TRUBACKUP_CONFIG_PATH",
    default="/etc/trubackup.json",
    help="Path to JSON file containing info about databases to dump",
)
