import os
import datetime

import click

import ...settings


@click.command()
def run():
    """Restore MongoDB from dump"""
    print("Restoring MongoDB")

    cmd = "mongorestore -h {host}:{port} -u {user} -p {password} --gzip --archive {input_path}".format(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        user=settings.MONGO_USER,
        password=settings.MONGO_PASSWORD,
        output_path=os.path.join(
            settings.MONGO_OUTPUT_DIR, input_file
        )
    ).split()

    cmd = " ".join(cmd)
    print("Running:")
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    run()
