import os
import datetime
from glob import iglob
import json
import sys

from functools import partial
import click

from swiftclient.service import SwiftUploadObject

from edxbackup.options import dbconfig_path_option
from edxbackup.options import dump_location_option
from edxbackup.swift import getSwiftService
from edxbackup.s3 import dump_s3, restore_s3


@dump_location_option(
    type=click.Path(exists=True, writable=True, file_okay=False, dir_okay=True)
)
@dbconfig_path_option
@click.command(name="edx_dump")
def dump(dump_location, dbconfig_path):
    """Dump Mysql and MongoDB databases relative to the given edX instance"""
    info = json.load(click.open_file(dbconfig_path))
    now = datetime.datetime.utcnow().isoformat()
    output_dir = os.path.join(dump_location, f"{now}")
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
        cmd = f"mydumper --compress {mysql_options(mysql_info)} -o {output_path}"
        print(f"Running:\n{cmd.replace(mysql_info['password'], '')}")
        if os.system(cmd) != 0:
            click.echo(f'Error dumping mysql db {mysql_info.get("dbname")}')

    if "s3" in info:
        click.echo("Dumping S3")
        output_path = os.path.join(output_dir, "s3.tar.gz")
        s3_host = info["s3"]["host"]
        s3_access_key = info["s3"]["access_key"]
        s3_secret_key = info["s3"]["secret_key"]
        s3_https = info["s3"]["https"]
        dump_s3(s3_host, s3_access_key, s3_secret_key, output_path, s3_https)

    if "swift" in info:
        to_upload = []
        for filepath in iglob(f"{output_dir}/**", recursive=True):
            if not os.path.isfile(filepath):
                continue
            to_upload.append(
                SwiftUploadObject(
                    filepath, object_name=f"{'/'.join(filepath.split('/')[2:])}"
                )
            )
        if "container" not in info["swift"]:
            click.echo("No container specified. Aborting")
            click.get_current_context().fail()
        container = info["swift"]["container"]
        print(f"Uploading via SWIFT to container {container}")
        with getSwiftService(info) as swift:
            # Consume the return value of swift.upload
            problems = [
                el
                for el in swift.upload(container, to_upload)
                if not el["success"] and el["action"] != "create_container"
            ]
        if problems:
            print("There were problems uploading the dump via swift")
            print(problems)
            sys.exit(-1)


@dump_location_option(type=click.Path(exists=True, file_okay=False, dir_okay=True))
@dbconfig_path_option
@click.command(name="edx_restore")
def restore(dump_location, dbconfig_path):
    """Restore Mysql and MongoDB databases relative to the given edX instance"""
    mongo_dump = "mongodb_dump_sql"
    mysql_dump = "mysql_dump"
    s3_dump    = "s3_dump.tar.gz"
    expected_content = [mongo_dump, mysql_dump, s3_dump]

    actual_content = sorted(os.listdir(dump_location))
    if set(actual_content) <= set(expected_content):
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
    cmd = f"mongorestore -h {mongo_host}:{mongo_port} --gzip --archive={mongo_path}"
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo("Error restoring mongo")
        click.get_current_context().fail()

    click.echo("Restoring mysql")
    options = mysql_options(info["mysql"])
    path = os.path.join(dump_location, "mysql_dump")
    cmd = f"myloader {options} --overwrite-tables --directory {path}"
    print(f"Running:\n{cmd.replace(info['mysql']['password'], '')}")
    if os.system(cmd) != 0:
        click.echo("Error restoring mysql")
        click.get_current_context().fail()

    if "s3" in info:
        click.echo("Restore S3")
        path = os.path.join(dump_location, "s3.tar.gz")
        s3_host = info["s3"]["host"]
        s3_access_key = info["s3"]["access_key"]
        s3_secret_key = info["s3"]["secret_key"]
        s3_https = info["s3"]["https"]
        restore_s3(s3_host, s3_access_key, s3_secret_key, path, s3_https)


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
