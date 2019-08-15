import click
from edxbackup import edx
from edxbackup import bookkeeping


@click.group(context_settings={"help_option_names": ["-h", "--help", "help"]})
def main():
    pass


main.add_command(edx.dump)
main.add_command(edx.restore)
main.add_command(bookkeeping.remove_old)


if __name__ == "__main__":
    main()
