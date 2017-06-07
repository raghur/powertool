# -*- coding: utf-8 -*-

import click
import logging
import coloredlogs

logger = logging.getLogger(__name__)

@click.command()
def list():
    click.echo("in list")

@click.command()
@click.option("-b", "--broadcast", default="192.168.1.255",
              help="machine ip's subnet")
@click.option("-h", "--host", help="hostname of your server")
@click.argument("mac", nargs=1)
def register(broadcast, host, mac):
    click.echo(broadcast)
    click.echo(host)
    click.echo(mac)
    click.echo("In register")

@click.command()
@click.argument('target', nargs=-1)
def wol(target):
    click.echo("In wake ")
    for t in target:
        click.echo(t)

@click.command()
@click.argument('target', nargs=-1)
def sleep(target):
    click.echo("In sleep ")
    for t in target:
        click.echo(t)


@click.group()
@click.option('-c', '--config', type=click.Path(), default='~/.powertool')
@click.option('-l', '--log', default="DEBUG", type=click.Choice(["INFO", "DEBUG",
                                               "WARNING", "ERROR",
                                               "CRITICAL", "NOTSET"]))
def main(log, config):
    """Console script for powertool"""
    if log and log != 'NOTSET':
        coloredlogs.install(level=log)
    click.echo(log)
    logger.debug('filename %s', config)
    logger.debug("Replace this message by putting your code into "
               "powertool.cli.main")
    logger.debug("See click documentation at http://click.pocoo.org/")

main.add_command(wol)
main.add_command(register)
main.add_command(sleep)
main.add_command(list)

if __name__ == "__main__":
    main(None)
