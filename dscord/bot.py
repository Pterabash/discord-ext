import os, sys
from importlib import import_module
from pydoc import plaintext, render_doc

from discord.ext import commands
from dscord import ext
from .func import code_wrap


client = commands.Bot(',')


def prefix(pf: str) -> None:
    global client
    client = commands.Bot(pf)


def load(name: str, package: str = 'dscord.ext') -> None:
    if package != '' and name[0] != '.':
        name = '.' + name
    module = import_module(name, package)
    module.setup(client)


def restart() -> None:
    os.execl(sys.executable, sys.executable, *sys.argv)


def run(token: str) -> None:
    client.run(token)


@client.command('exts')
async def extList(ctx):
    ext_doc = render_doc(ext, 'Help on %s', renderer=plaintext)
    for x in code_wrap(ext_doc): await ctx.send(x)


@client.command('load')
async def extLoad(ctx, module: str) -> None:
    load('.'+module, 'dscord.ext')
    await ctx.send(f'`{module}` loaded')


@client.command('restart', aliases=['respawn', 'retard'])
async def botRestart(ctx) -> None:
    await ctx.send('Restarting')
    restart()


@client.command('update', aliases=['upgrade'])
async def botUpdate(ctx) -> None:
    await ctx.send('Updating')
    os.system('pip3 install git+https://github.com/thisgary/dscord')
    await ctx.send('Success & restarting')
    restart()
