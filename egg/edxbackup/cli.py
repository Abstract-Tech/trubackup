import click
from edxbackup import mongo
from edxbackup import mysql


@click.group(context_settings={'help_option_names': ['-h', '--help', 'help']})
def main():
    pass


main.add_command(mysql.dump)
main.add_command(mysql.restore)
main.add_command(mongo.dump)
main.add_command(mongo.restore)


if __name__ == "__main__":
    main()
