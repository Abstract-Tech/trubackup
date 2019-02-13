import os
import datetime

import click

from edxbackup import options


@click.command(name="mongo_dump")
@options.mongo_host
@options.mongo_port
@options.database
@options.output_dir
def dump(mongo_host, mongo_port, database, output_dir):
    """Dumps MongoDB"""
    # TODO: use a different strategy according to the mongodb version
    print("Dumping MongoDB")
    now = datetime.datetime.now().strftime(options.DUMP_FILENAME_DATE_FORMAT)
    output_filename = f"{now}-dump.sql.gz"
    output_path = os.path.join(output_dir, output_filename)
    cmd = f"mongodump -h {mongo_host}:{mongo_port} -d {database} --gzip --archive={output_path}"

    if database:
        cmd += f" -d {database}"
    print("Running:")
    print(cmd)
    os.system(cmd)


@click.command(name="mongo_restore")
@options.mongo_host
@options.mongo_port
@options.input_file
def restore(mongo_host, mongo_port, input_file):
    """Restore MongoDB from dump"""
    echo_g("Restoring MongoDB")
    # TODO: use a different strategy according to the mongodb version

    # Extract tarball to /tmp
    echo_g('Extracting tarball')
    os.system(f'tar xf {input_file} -C /tmp')
    # XXX assuming the archive file we're passed contains a single mongodump directory
    echo_g('Invoking Mongorestore')
    os.system(f"mongorestore -v -h {mongo_host}:{mongo_port} /tmp/mongodump")

def echo_g(text):
    """Shortcut to make text green"""
    click.echo(click.style(text, fg='green'))