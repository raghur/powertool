# -*- coding: utf-8 -*-

from  io import open
import json
import os
import re
import logging
import click
import coloredlogs
from wakeonlan import wol

logger = logging.getLogger(__name__)

def save_config(ctx, log, config):
    logger.debug("In result callback: %s "% ctx)
    if not ctx:
        return
    logger.debug("In result callback: %s "% config)
    file = os.path.expanduser(config)
    logger.debug("Config updated - writing to file")
    with open(file, "w") as fh:
        json.dump(ctx.obj["config"], fh)

@click.group(result_callback=save_config)
@click.option('-c', '--config', type=click.Path(), default='~/.powertool')
@click.option('-l', '--log', default="DEBUG", type=click.Choice([
    "INFO", "DEBUG",
    "WARNING", "ERROR",
    "CRITICAL", "NOTSET"]))
@click.pass_context
def main(ctx, log, config):
    # print("in main")
    # print(ctx)
    # print(log)
    # print(config)
    """Console script for powertool"""
    if log and log != 'NOTSET':
        coloredlogs.install(level=log)
    click.echo(log)
    logger.debug('filename %s', config)
    file=createIfNotExists(config)
    with open(file, "r") as fh:
        machines = json.load(fh)
    # logger.debug(ctx, ctx.obj)
        ctx.obj = {}
        ctx.obj['config'] = machines
        hostmap = {}
        for mac, machine in machines.items():
            if 'hostname' in machine:
                hostmap[machine['hostname']] = mac
        ctx.obj['hostmapping'] = hostmap
        logger.debug("Built hostmap: %s" % hostmap)

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
    config = ctx.obj["config"]
    [print("%s\t%s\t%s" % (config[k]["hostname"],
                           k,
                           config[k]["broadcast"])) for k in config.keys()]

def validate_broadcast(ctx, param, value):
    logger.debug("In validate_broadcast: %s" % value)
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",value):
        raise click.BadParameter("broadcast needs to be an IP address")
    return value

def validate_mac(ctx, param, value):
    if not value:
        return
    logger.debug("In validate_mac: %s" % value)
    if not re.match(r"([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}",value):
        raise click.BadParameter("broadcast needs to be a mac address")
    return value

@main.command()
@click.option("-b", "--broadcast",
              default="192.168.1.255",
              callback=validate_broadcast,
              help="machine ip's subnet")
@click.option("-h", "--host", help="hostname of your server")
@click.argument("mac", nargs=1, callback=validate_mac)
@click.pass_context
def register(ctx, broadcast, host, mac):
    click.echo(broadcast)
    click.echo(host)
    click.echo(mac)
    machines = ctx.obj["config"]
    machines[mac] = {"hostname": host, "broadcast":broadcast}
    click.echo("In register")
    return ctx

@main.command()
@click.option("-h", "--host", help="hostname of your server")
@click.option("-m", "--mac", callback=validate_mac)
@click.pass_context
def rm(ctx, host, mac):
    config = ctx.obj["config"]
    if mac:
        config.pop(mac, None)
    else:
        keysToRemove=[]
        for key in config.keys():
            if host == config[key]["hostname"]:
                keysToRemove += [key]
        logger.debug("Keys to remove: %s", keysToRemove)
        for key in keysToRemove:
            config.pop(key)
    return ctx

@main.command()
@click.argument('target', nargs=-1)
@click.pass_context
def wake(ctx, target):
    click.echo(ctx.obj["config"])
    click.echo("In wake ")
    config = ctx.obj["config"]
    hostmap = ctx.obj['hostmapping']
    for t in target:
        logger.debug("Waking host: %s" % t)
        if t not in hostmap:
            logger.warn("No hostname found for %s" % t)
            continue
        mac = hostmap[t]
        logger.debug("sending magic packet to %s:%s ip:%s" % (t,
                     mac,
                     config[mac]['broadcast']))
        wol.send_magic_packet(mac, ip_address=config[mac]['broadcast'])



@main.command()
@click.argument('target', nargs=-1)
def sleep(target):
    click.echo("In sleep ")
    for t in target:
        click.echo(t)

