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
    """Dumps MySQL"""
    print("Dumping MySQL")
    cmd = "mysqldump -h {host} -u {user} -p{password} -P {port}".format(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD
    ).split()

    if not database:
        cmd.append("--all-databases")
    else:
        cmd.extend(["-d", database])

    if not settings.MYSQL_SOCKET:
        cmd.extend(["--protocol", "tcp"])

    ensure_directory_exists(settings.MYSQL_OUTPUT_DIR)
    output_file = "{now}-dump.sql.gz".format(
        now=datetime.datetime.now().strftime(
            settings.DUMP_FILENAME_DATE_FORMAT
        )
    )
    output_path = os.path.join(
        settings.MYSQL_OUTPUT_DIR,
        output_file
    )

    cmd.extend([
        "|", "gzip --best > {}".format(output_path)
    ])

    cmd = " ".join(cmd)
    print("Running:")
    print(cmd)
    os.system(cmd)

    print("Successfully dumped MySQL to {}".format(output_path))


if __name__ == '__main__':
    run()
