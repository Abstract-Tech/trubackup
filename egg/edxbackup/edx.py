import os
import datetime
import json
import sys

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


@dump_location_option(
    type=click.Path(exists=True, writable=True, file_okay=False, dir_okay=True)
)
@dbconfig_path_option
@click.command(name="edx_dump")
def dump(dump_location, dbconfig_path):
    """Dump Mysql and MongoDB databases relative to the given edX instance"""
    info = json.load(click.open_file(dbconfig_path))
    now = datetime.datetime.now().isoformat()
    output_dir = os.path.join(dump_location, f"edxdump-{now}")
    click.echo(f"Creating dumps in {output_dir}")
    os.mkdir(output_dir)

    click.echo("Dumping mongodb")
    output_path = os.path.join(output_dir, "mongodb_dump.gz")
    mongo_host = info["mongo"]["host"]
    mongo_port = info["mongo"]["port"]
    cmd = f"mongodump -h {mongo_host}:{mongo_port} " f"--gzip --archive={output_path}"
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo("Error dumping mongo")

    click.echo("Dumping mysql")
    output_path = os.path.join(output_dir, "mysql_dump")
    for mysql_info in info["mysql"]:
        cmd = f"mydumper {mysql_options(mysql_info)} -o {output_path}"
        print(f"Running:\n{cmd}")
        if os.system(cmd) != 0:
            click.echo(f'Error dumping mysql db {mysql_info.get("dbname")}')


@dump_location_option(type=click.Path(exists=True, file_okay=False, dir_okay=True))
@dbconfig_path_option
@click.command(name="edx_restore")
def restore(dump_location, dbconfig_path):
    """Restore Mysql and MongoDB databases relative to the given edX instance"""
    expected_content = ["mongodb_dump.gz", "mysql_dump"]
    actual_content = sorted(os.listdir(dump_location))
    if actual_content != expected_content:
        click.echo(
            f"The directory {dump_location} does not contain "
            f"the expected files ({expected_content})\n"
            f"These files were found instead:\n{actual_content}"
        )
        sys.exit(1)
    info = json.load(click.open_file(dbconfig_path))
    click.echo(f"Restoring dump from {dump_location}")

    click.echo("Restoring mongodb")
    mongo_path = os.path.join(dump_location, "mongodb_dump.gz")
    mongo_host = info["mongo"]["host"]
    mongo_port = info["mongo"]["port"]
    cmd = f"mongorestore -h {mongo_host}:{mongo_port} " f"--gzip --archive={mongo_path}"
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo("Error restoring mongo")
        click.get_current_context().fail()

    click.echo("Restoring mysql")
    options = mysql_options(info["mysql"])
    path = os.path.join(dump_location, "mysql_dump")
    cmd = f"myloader {options} --overwrite-tables --directory {path}"
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo("Error restoring mysql")
        click.get_current_context().fail()


def mysql_options(mysql_info):
    """Return a string to be used with mydumper/myloader
    given an mysql `info` dict.
    """
    result = (
        f"--host {mysql_info['host']} --user {mysql_info['user']} "
        f"--password {mysql_info['password']} --port {mysql_info['port']} "
    )
    if "dbname" in mysql_info:
        result += f" -B {mysql_info['dbname']} "
    return result
