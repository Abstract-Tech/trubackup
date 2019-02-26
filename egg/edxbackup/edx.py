import os
import datetime

import click

from edxbackup import options


edx_config = click.option(
    "--edx-config",
    envvar="EDX_CONFIG",
    default='-',
    help="Path to lms.auth.json or cms.auth.json",
)


@edx_config
@click.command(name="edx_dump")
def dump(edx_config):
    """Dump Mysql and MongoDB databases relative to the given edX instance"""
    config = click.open_file(edx_config).read()


@edx_config
@click.command(name="edx_restore")
def restore(edx_config):
    """Restore Mysql and MongoDB databases relative to the given edX instance"""


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
