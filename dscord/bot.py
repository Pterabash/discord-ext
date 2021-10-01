import os
import importlib
import pydoc
import sys

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
    module = importlib.import_module(name, package)
    module.setup(client)


def run(token: str) -> None:
    client.run(token)


@client.command('exts')
async def botExtList(ctx):
    ext_doc = pydoc.render_doc(ext, 'Help on %s', renderer=pydoc.plaintext)
    for x in code_wrap(ext_doc): await ctx.send(x)


@client.command('load')
async def botExtLoad(ctx, module: str) -> None:
    load('.'+module, 'dscord.ext')
    await ctx.send(f'`{module}` loaded')


@client.command('restart', aliases=['retard', 'reboot', 'update', 'upgrade'])
async def botRestart(ctx) -> None:
    await ctx.send('Updating')
    os.system('pip3 install git+https://github.com/thisgary/dscord')
    await ctx.send('Finished updating. Restarting...')
    os.execl(sys.executable, sys.executable, *sys.argv)
