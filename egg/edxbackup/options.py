import click
from functools import partial

option = partial(click.option, show_envvar=True, show_default=True)
DUMP_FILENAME_DATE_FORMAT = "%d-%m-%y_%H-%M-%S"


mysql_host = option(
    "--mysql-host",
    envvar="MYSQL_HOST",
    default='localhost',
    help="IP Address of the MySQL server"
)
mysql_port = option(
    "--mysql-port",
    envvar="MYSQL_PORT",
    default='3306',
    help="IP port of the MySQL server"
)
mysql_user = option(
    "--mysql-user",
    envvar="MYSQL_USER",
    required=True,
    help="MySQL server user"
)
mysql_password = option(
    "--mysql-password",
    envvar="MYSQL_PASSWORD",
    required=True,
    help="MySQL server password"
)

mongo_host = option(
    "--mongo-host",
    envvar="MONGO_HOST",
    default='localhost',
    help="IP Address of the MongoDB server"
)
mongo_port = option(
    "--mongo-port",
    envvar="MONGO_PORT",
    default='27017',
    help="IP port of the MongoDB server"
)
mongo_user = option(
    "--mongo-user",
    envvar="MONGO_USER",
    required=True,
    help="MongoDB server user"
)
mongo_password = option(
    "--mongo-password",
    envvar="MONGO_PASSWORD",
    required=True,
    help="MongoDB server password"
)



input_file = option(
    '--input-file',
    type=click.Path(exists=True, readable=True),
    required=True,
    )
output_dir = option(
    '--output-dir',
    envvar="OUTPUT_DIR",
    type=click.Path(exists=True, writable=True),
    required=True,
    )

database = option('--database', help="Dump a single database")
