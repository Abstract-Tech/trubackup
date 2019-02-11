import os
import datetime

import click

import ...settings


@click.command()
@click.argument('input_file')
def run(input_file):
    """Restore MySQL from dump"""
    print("Restoring MySQL")

    cmd = "gunzip < {input_file} | mysql -h {host} -P {port} -u {user} -p{password}".format(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        input_file=input_file
    ).split()

    if not settings.MYSQL_SOCKET:
        cmd.extend(["--protocol", "tcp"])

    cmd = " ".join(cmd)
    print("Running:")
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    run()
