import click
from edxbackup import edx


@click.group(context_settings={"help_option_names": ["-h", "--help", "help"]})
def main():
    pass


main.add_command(edx.dump)
main.add_command(edx.restore)


if __name__ == "__main__":
    main()
