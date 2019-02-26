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
    if os.system(cmd) != 0:
        click.echo('Error dumping mongo')

    click.echo('Dumping mysql')
    options = mysql_options(info)
    output_path = os.path.join(output_dir, 'mysql_dump.sql.gz')
    cmd = (f"mysqldump --all-databases --protocol tcp {options}"
        f"|gzip -6 - >{output_path}")
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo('Error dumping mysql')


@dump_location(
    type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@edx_config
@click.command(name="edx_restore")
def restore(dump_location, edx_config):
    """Restore Mysql and MongoDB databases relative to the given edX instance"""
    expected_content = ['mongodb_dump.gz', 'mysql_dump.sql.gz']
    actual_content = sorted(os.listdir(dump_location))
    if actual_content != expected_content:
        click.echo(f'The directory {dump_location} does not contain '
            f'the expected files ({expected_content})\n'
            f'These files were found instead:\n{actual_content}')
        sys.exit(1)
    info = extract_info(json.load(click.open_file(edx_config)))
    click.echo(f'Restoring dump from {dump_location}')

    click.echo('Restoring mongodb')
    mongo_path = os.path.join(dump_location, 'mongodb_dump.gz')
    mongo_host = info['mongo'][0]['host']
    mongo_port = info['mongo'][0]['port']
    cmd = (
        f"mongorestore -h {mongo_host}:{mongo_port} "
        f"--gzip --archive={mongo_path}")
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo('Error restoring mongo')

    click.echo('Restoring mysql')
    options = mysql_options(info)
    path = os.path.join(dump_location, 'mysql_dump.sql.gz')
    cmd = f"zcat {path}|mysql  --protocol tcp {options}"
    print(f"Running:\n{cmd}")
    if os.system(cmd) != 0:
        click.echo('Error dumping mysql')



def mysql_options(info):
    """Return a string to be used with mysqldump/restore
    given an `info` dict as returned by `extract_info`.
    """
    mysql_host = info['mysql'][0]['host']
    mysql_port = info['mysql'][0]['port']
    mysql_port = info['mysql'][0]['port']
    mysql_user = info['mysql'][0]['user']
    mysql_password = info['mysql'][0]['password']
    return (f"-h {mysql_host} -u {mysql_user} "
        f"-p{mysql_password} -P {mysql_port} ")


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
