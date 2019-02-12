import os
import datetime

import click
from edxbackup import options


@click.command(name='mysql_restore')
@options.mysql_host
@options.mysql_port
@options.mysql_user
@options.mysql_password
@options.input_file
def restore(mysql_host, mysql_port, mysql_user, mysql_password, input_file):
    """Restore MySQL from dump"""
    print("Restoring MySQL")

    cmd = f"gunzip < {input_file} | mysql -h {mysql_host} -P {mysql_port} -u {mysql_user} -p{mysql_password} --protocol tcp"
    print("Running:")
    print(cmd)
    os.system(cmd)


@click.command(name='mysql_dump')
@options.mysql_host
@options.mysql_port
@options.mysql_user
@options.mysql_password
@options.database
@options.output_dir
def dump(mysql_host, mysql_port, mysql_user, mysql_password, database, output_dir):
    """Dumps MySQL"""
    print("Dumping MySQL")
    cmd = f"mysqldump --protocol tcp -h {mysql_host} -u {mysql_user} -p{mysql_password} -P {mysql_port}"

    if not database:
        cmd += " --all-databases"
    else:
        cmd += f" -d {database}"
    now=datetime.datetime.now().strftime(options.DUMP_FILENAME_DATE_FORMAT)
    output_path = os.path.join(output_dir, f"{now}-dump.sql.gz")
    cmd += f'|gzip -6 - >{output_path}'

    print("Running:")
    print(cmd)
    os.system(cmd)

    print("Successfully dumped MySQL to {}".format(output_path))
