import click

from edxbackup.options import dbconfig_path_option
from edxbackup.options import dump_location_option


@dump_location_option(type=click.Path(exists=True, readable=True))
@dbconfig_path_option
@click.command(name="remove_old")
def remove_old(dump_location, dbconfig_path):
    pass
