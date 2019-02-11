import os
import datetime

import click

import ...settings
from ..utils import ensure_directory_exists

@click.command()
@click.option(
    '--database',
    help="Dump a single database",
    required=False
)
def run(
    database=None
):
    """Dumps MongoDB"""
    print("Dumping MongoDB")

    ensure_directory_exists(settings.MONGO_OUTPUT_DIR)
    output_file = "{now}-dump.sql.gz".format(
        now=datetime.datetime.now().strftime(
            settings.DUMP_FILENAME_DATE_FORMAT
        )
    )

    cmd = "mongodump -h {host}:{port} -d {database} --gzip --archive={output_path}".format(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        database=settings.MONGO_DATABASE,
        output_path=os.path.join(
            settings.MONGO_OUTPUT_DIR, output_file
        )
    ).split()

    if database:
        cmd.extend(["-d", database])

    cmd = " ".join(cmd)
    print("Running:")
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    run()
