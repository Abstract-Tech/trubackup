import os
import datetime

import click


@click.command(name='mysql_restore')
@click.argument('input_file')
def restore(input_file):
    """Restore MySQL from dump"""
    print("Restoring MySQL")

    cmd = "gunzip < {input_file} | mysql -h {host} -P {port} -u {user} -p{password}".format(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        input_file=input_file
    ).split()

    if not settings.MYSQL_SOCKET:
        cmd.extend(["--protocol", "tcp"])

    cmd = " ".join(cmd)
    print("Running:")
    print(cmd)
    os.system(cmd)


@click.command(name='mysql_dump')
@click.option('--database', help="Dump a single database", required=False)
def dump(database=None):
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
