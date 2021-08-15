import os, sys
from importlib import import_module
from pydoc import plaintext, render_doc

from discord.ext import commands

from dscord import ext
from .func import code_wrap

bot = commands.Bot(',')


@bot.command('exts')
async def extList(ctx):
    ext_doc = render_doc(ext, 'Help on %s', renderer=plaintext)
    for x in code_wrap(ext_doc): await ctx.send(x)


@bot.command('load')
async def extLoad(ctx, module: str):
    load('.'+module, 'dscord.ext')
    await ctx.send(f'`{mdl}` loaded')


@bot.command('restart', aliases=['respawn', 'retard'])
async def botRestart(ctx):
    await ctx.send('Restarting')
    restart()


@bot.command('update', aliases)
async def botUpdate(ctx):
    await ctx.send('Updating')
    os.system('pip3 install git+https://github.com/thisgary/dscord')
    await ctx.send('Success & restarting')
    restart()


def restart():
    os.execl(sys.executable, sys.executable, *sys.argv)


def load(name: str, package: str = None):
    if package and name[0] != '.':
        name = '.' + name
    module = import_module(name, package)
    module.setup(client)


def run(token: str):
    client.run(token)
