import os
import datetime
from glob import iglob
import json
import sys

from functools import partial
import click

from swiftclient.service import SwiftUploadObject

from edxbackup.config import EdxbackupConfig
from edxbackup.options import dbconfig_path_option
from edxbackup.options import dump_location_option
from edxbackup.mysql import dump_mysql_db, restore_mysql_db
from edxbackup.mongo import dump_mongo_db, restore_mongo_db
from edxbackup.swift import getSwiftService
from edxbackup.s3 import dump_s3, restore_s3


@dump_location_option(
    type=click.Path(exists=True, writable=True, file_okay=False, dir_okay=True)
)
@dbconfig_path_option
@click.command(name="edx_dump")
def dump(dump_location, dbconfig_path):
    """Dump Mysql and MongoDB databases relative to the given edX instance"""
    info = EdxbackupConfig(**json.load(click.open_file(dbconfig_path)))

    now = datetime.datetime.utcnow().isoformat()
    output_dir = os.path.join(dump_location, f"{now}")
    click.echo(f"Creating dump in {output_dir}")
    os.mkdir(output_dir)

    click.echo("Dumping mongodb")
    for mongo_info in info.mongo:
        dump_mongo_db(mongo_info, output_dir)

    click.echo("Dumping mysql")
    for mysql_info in info.mysql:
        dump_mysql_db(mysql_info, output_dir)

    click.echo("Dumping S3")
    if info.s3 is not None:
        dump_path = os.path.join(output_dir, "s3.tar.gz")
        dump_s3(
            info.s3.host,
            info.s3.access_key,
            info.s3.secret_key,
            dump_path,
            info.s3.https,
        )

    click.echo("Uploading dump")
    if info.swift is not None:
        to_upload = []
        for filepath in iglob(f"{output_dir}/**", recursive=True):
            if not os.path.isfile(filepath):
                continue
            to_upload.append(
                SwiftUploadObject(
                    filepath, object_name=f"{'/'.join(filepath.split('/')[2:])}"
                )
            )
        print(f"Uploading via SWIFT to container {info.swift.container}")
        with getSwiftService(info) as swift:
            # Consume the return value of swift.upload
            problems = [
                el
                for el in swift.upload(info.swift.container, to_upload)
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
    info = EdxbackupConfig(**json.load(click.open_file(dbconfig_path)))
    click.echo(f"Restoring dump from {dump_location}")

    click.echo("Restoring mongodb")
    for mongo_info in info.mongo:
        restore_mongo_db(mongo_info, dump_location)

    click.echo("Restoring mysql")
    for mysql_info in info.mysql:
        restore_mysql_db(mysql_info, dump_location)

    click.echo("Restoring S3")
    if info.s3 is not None:
        dump_path = os.path.join(dump_location, "s3.tar.gz")
        restore_s3(
            info.s3.host,
            info.s3.access_key,
            info.s3.secret_key,
            dump_path,
            info.s3.https,
        )
