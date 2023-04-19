from edxbackup import backup
from edxbackup import info
from edxbackup import restore

import click
import os


RESTIC_VARS = ["RESTIC_REPOSITORY", "RESTIC_PASSWORD"]


@click.group(context_settings={"help_option_names": ["-h", "--help", "help"]})
def main() -> None:
    if not set(os.environ.keys()).issuperset(RESTIC_VARS):
        click.echo(
            f"Environment variables must be set for edxbackup to work: {RESTIC_VARS}"
        )


main.add_command(backup.perform_backup)
main.add_command(restore.perform_restore)

main.add_command(info.list_groups)
main.add_command(info.show_group)


if __name__ == "__main__":
    main()
