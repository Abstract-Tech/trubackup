import click

root = click.option(
    "-mh", "--mysql_host",
    envvar="MYSQL_HOST",
    default='localhost', show_default=True,
    help="IP Address of the MySQL server"
)

