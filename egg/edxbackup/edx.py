import os
import datetime
import json
import sys

import click
from functools import partial

from edxbackup import options


edx_config = click.option(
    "--edx-config",
    envvar="EDX_CONFIG",
    required=True,
    help="Path to lms.auth.json or cms.auth.json",
)


dump_location = partial(click.option,
    "--dump-location",
    envvar="DUMP_LOCATION",
    required=True,
    help="Path where the dump will be read or written to",
)


@dump_location(
    type=click.Path(exists=True, writable=True, file_okay=False, dir_okay=True)
)
@edx_config
@click.command(name="edx_dump")
def dump(dump_location, edx_config):
    """Dump Mysql and MongoDB databases relative to the given edX instance"""
    info = extract_info(json.load(click.open_file(edx_config)))
    now = datetime.datetime.now().isoformat()
    output_dir = os.path.join(dump_location, f'edxdump-{now}')
    click.echo(f'Creating dumps in {output_dir}')
    os.mkdir(output_dir)

    click.echo('Dumping mongodb')
    output_path = os.path.join(output_dir, 'mongodb_dump.gz')
    mongo_host = info['mongo'][0]['host']
    mongo_port = info['mongo'][0]['port']
    cmd = (
        f"mongodump -h {mongo_host}:{mongo_port} "
        f"--gzip --archive={output_path}")
    print(f"Running:\n{cmd}")
    os.system(cmd)

    click.echo('Dumping mysql')
    mysql_host = info['mysql'][0]['host']
    mysql_port = info['mysql'][0]['port']
    mysql_port = info['mysql'][0]['port']
    mysql_user = info['mysql'][0]['user']
    mysql_password = info['mysql'][0]['password']
    output_path = os.path.join(output_dir, 'mysql_dump.sql.gz')
    cmd = (f"mysqldump --all-databases --protocol tcp "
        f"-h {mysql_host} -u {mysql_user} "
        f"-p{mysql_password} -P {mysql_port} "
        f"|gzip -6 - >{output_path}")
    print(f"Running:\n{cmd}")
    os.system(cmd)


@dump_location(
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@edx_config
@click.command(name="edx_restore")
def restore(dump_location, edx_config):
    """Restore Mysql and MongoDB databases relative to the given edX instance"""
    info = extract_info(json.load(click.open_file(edx_config)))


def extract_info(json_content):
    """Extract info about mongodb and mysql databases used by an edx instance.
    It accepts a python dictionary containing the json-decoded info from
    lms.auth.json or cms.auth.json file.

    Returns a dictionary with the following structure:

    {
        "mysql": [{
            "dbname": "edx",
            "host": "localhost",
            "user": "mysql_user",
            "password": "mysql_password",
            "port": "3306",
        }],
        "mongo": [{
            "dbname": "edx",
            "host": "localhost",
            "user": "mongo_user",
            "password": "mongo_password",
            "port": "3306",
        }]
    }
    """
    result = dict(mysql=[], mongo=[])
    result['mysql'] = extract_mysql_info(json_content)
    result['mongo'] = extract_mongo_info(json_content)
    return result


def extract_mysql_info(json_content):
    result = []
    for name, info in json_content['DATABASES'].items():
        el = dict(
            dbname=info['NAME'],
            host=info['HOST'],
            user=info['USER'],
            password=info['PASSWORD'],
            port=info['PORT'],
            )
        if el not in result:
            result.append(el)
    return result


def extract_mongo_info(json_content):
    conf = json_content['DOC_STORE_CONFIG']
    return [dict(
        dbname=conf['db'],
        host=conf['host'][0],
        user=conf['user'],
        password=conf['password'],
        port=conf['port'],
    )]
