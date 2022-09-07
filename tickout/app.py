# -*- coding:utf-8 -*-
import sys
import typing as ty
import click
from .settings import settings as SETTINGS
from .log import LOG


def setup():
    if SETTINGS.FLOMO_SDK:
        sys.path.append(SETTINGS.FLOMO_SDK)
        LOG.debug("Loaded Flomo SDK: %(sdk_path)s", extra=dict(
            sdk_path = SETTINGS.FLOMO_SDK,
        ))

    



@click.group()
@click.option('--settings', '-c', default=None, help='Path to config file.')
def cli(settings: ty.Optional[str] = None):
    if settings:
        SETTINGS.configure(settings)


    setup()


@cli.command()
def shell():
    try:
        import IPython
        shell = IPython.terminal.embed.InteractiveShellEmbed()
        shell(local_ns=dict(
            settings = SETTINGS
        ))
    except ImportError:
        import code
        code.interact(local=dict(
            settings = SETTINGS
        ))
