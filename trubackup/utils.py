from typing import Any

import click


def log(obj: Any) -> None:
    "Plain print to stdout"
    click.echo(obj)


def log_success(obj: Any) -> None:
    "Print to stdout to emphasise successful operation"
    click.echo(click.style(obj, fg="green"))


def log_failure(obj: Any) -> None:
    "Print to stdout to emphasise failed operation"
    click.echo(click.style(obj, fg="red"))
