# -*- coding: utf-8 -*-

import click
import logging
import coloredlogs
from  io import open
import json
import os

logger = logging.getLogger(__name__)

@click.group()
@click.option('-c', '--config', type=click.Path(), default='~/.powertool')
@click.option('-l', '--log', default="DEBUG", type=click.Choice(["INFO", "DEBUG",
                                               "WARNING", "ERROR",
                                               "CRITICAL", "NOTSET"]))
@click.pass_context
def main(ctx, log, config):
    """Console script for powertool"""
    if log and log != 'NOTSET':
        coloredlogs.install(level=log)
    click.echo(log)
    logger.debug('filename %s', config)
    # logger.debug(ctx, ctx.obj)
    ctx.obj['config'] = config;
    click.echo("Replace this message by putting your code into "
               "powertool.cli.main")
    logger.debug("See click documentation at http://click.pocoo.org/")

def createIfNotExists(file):
    file = os.path.expanduser(file)
    if not os.path.exists(file):
        with open(file, "w") as outhandle:
            outhandle.write("{}")
    return file

@main.command()
@click.pass_context
def list(ctx):
    file = createIfNotExists(ctx.obj["config"])
    with open(file, "r") as fh:
        config = json.load(fh)
        [print("%s\t%s\t%s" % (config[k]["hostname"],
                               k,
                               config[k]["broadcast"])) for k in config.keys()]

@main.command()
@click.option("-b", "--broadcast", default="192.168.1.255",
              help="machine ip's subnet")
@click.option("-h", "--host", help="hostname of your server")
@click.argument("mac", nargs=1)
@click.pass_context
def register(ctx, broadcast, host, mac):
    click.echo(broadcast)
    click.echo(host)
    click.echo(mac)
    file=createIfNotExists(ctx.obj["config"])
    logger.debug(file);
    with open(file, "r") as fh:
        machines = json.load(fh)
    with open(file, "w") as fh:
        machines[mac] = {"hostname": host, "broadcast":broadcast}
        json.dump(machines, fh)
    click.echo("In register")

@main.command()
@click.argument('target', nargs=-1)
@click.pass_context
def wol(ctx, target):
    click.echo(ctx.obj["config"])
    click.echo("In wake ")
    for t in target:
        click.echo(t)

@main.command()
@click.argument('target', nargs=-1)
def sleep(target):
    click.echo("In sleep ")
    for t in target:
        click.echo(t)


def cli():
    main({})
