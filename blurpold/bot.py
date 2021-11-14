import os
import importlib
import pydoc
import sys

from discord.ext import commands

from blurpold import ext
from blurpold.func import send_embed, wrap


client = commands.Bot(',')


def prefix(pf: str) -> None:
    global client
    client = commands.Bot(pf)


def load(name: str, package: str = 'blurpold.ext') -> None:
    if not name.startswith('.') and package != '':
        name = '.' + name
    module = importlib.import_module(name, package)
    module.setup(client)


def run(token: str) -> None:
    client.run(token)


@client.command('load')
async def command_ext_load(ctx, module: str) -> None:
    load('.'+module, 'blurpold.ext')
    await ctx.send(f'`{module}` loaded')


@client.command('exts')
async def command_ext_list(ctx):
    doc = pydoc.render_doc(ext, 'Help on %s', renderer=pydoc.plaintext)
    chunks = wrap(doc)
    send_embed(ctx.channel.id, chunks, title='Extensions List')


@client.command(aliases=['retard', 'reboot'])
async def restart(ctx, flag: str = None) -> None:
    if flag != 'skip': # if  flag == 'u':
        await ctx.send('Updating')
        os.system('pip3 install git+https://github.com/thisgary/blurpold')
    await ctx.send('Restarting')
    os.execl(sys.executable, sys.executable, *sys.argv)


@client.event
async def on_ready() -> None:
    print('Bot is up!')


@client.event
async def on_command_error(ctx, err) -> None:
    if (isinstance(err, commands.CommandNotFound) 
        or isinstance(err, commands.CheckFailure)): return
    print(err)
    log = wrap(str(err), code='bash')
    send_embed(ctx.channel.id, log, title='Error', color=0xe74c3c)
