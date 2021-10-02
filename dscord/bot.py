import os
import importlib
import pydoc
import sys

from discord.ext import commands

import dscord


client = commands.Bot(',')


def bot_prefix(pf: str) -> None:
    global client
    client = commands.Bot(pf)


def bot_run(token: str) -> None:
    client.run(token)


def ext_load(name: str, package: str = 'dscord.ext') -> None:
    if not name.startswith('.') and package != '':
        name = '.' + name
    module = importlib.import_module(name, package)
    module.setup(client)


@client.command('load')
async def command_ext_load(ctx, module: str) -> None:
    ext_load('.'+module, 'dscord.ext')
    await ctx.send(f'`{module}` loaded')


@client.command('exts')
async def command_ext_list(ctx):
    doc = pydoc.render_doc(
        dscord.ext, 'Help on %s', renderer=pydoc.plaintext
    )
    dscord.func.send_embed(doc)


@client.command(aliases=['retard', 'reboot', 'update', 'upgrade'])
async def restart(ctx, flag: str = None) -> None:
    if flag != 'skip': # Will reverse after official
        await ctx.send('Updating')
        os.system('pip3 install git+https://github.com/thisgary/dscord')
    await ctx.send('Restarting')
    os.execl(sys.executable, sys.executable, *sys.argv)
