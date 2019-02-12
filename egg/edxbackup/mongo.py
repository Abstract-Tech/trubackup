import os
import datetime

import click

from edxbackup import options


@click.command(name='mongo_dump')
@options.mongo_host
@options.mongo_port
@options.database
@options.output_dir
def dump(mongo_host, mongo_port, database, output_dir):
    """Dumps MongoDB"""
    print('Dumping MongoDB')
    now = datetime.datetime.now().strftime(options.DUMP_FILENAME_DATE_FORMAT)
    output_filename = f"{now}-dump.sql.gz"
    output_path = os.path.join(output_dir, output_filename)
    cmd = f"mongodump -h {mongo_host}:{mongo_port} -d {database} --gzip --archive={output_path}"

    if database:
        cmd += f' -d {database}'
    print("Running:")
    print(cmd)
    os.system(cmd)


@click.command(name='mongo_restore')
@options.mongo_host
@options.mongo_port
@options.mongo_user
@options.mongo_password
@options.input_file
def restore(mongo_host, mongo_port, mongo_user, mongo_password, input_file):
    """Restore MongoDB from dump"""
    print("Restoring MongoDB")

    cmd = f"mongorestore -h {mongo_host}:{mongo_port} -u {mongo_user} -p {mongo_password} --gzip --archive {input_file}"

    print("Running:")
    print(cmd)
    os.system(cmd)
