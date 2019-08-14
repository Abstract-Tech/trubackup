from functools import partial

import click


dbconfig_path_option = click.option(
    "--dbconfig-path",
    envvar="DBCONFIG_PATH",
    default="/etc/edxbackup.json",
    help="Path to JSON file containing info about databases to dump",
)


dump_location_option = partial(
    click.option,
    "--dump-location",
    envvar="DUMP_LOCATION",
    default="/destination",
    help="Path where the dump will be read or written to",
)
