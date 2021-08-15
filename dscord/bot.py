from importlib import import_module
from os import execl
from pydoc import render_doc, plaintext
from sys import executable, argv

from discord.ext import commands

from dscord import ext
from .func import code_wrap

client = commands.Bot(',')


@client.command('exts')
async def extList(ctx):
    ext_doc = render_doc(ext, 'Help on %s', renderer=plaintext)
    for x in code_wrap(ext_doc): await ctx.send(x)


@client.command('load')
async def extLoad(ctx, mdl: str):
    load(mdl)
    await ctx.send(f'`{mdl}` loaded')


@client.command(aliases=['respawn', 'retard'])
async def restart(self, ctx):
    await ctx.send('Restarting')
    execl(executable, executable, *argv)


def load(mdl: str, lib: str = 'dscord.ext'):
    module = import_module('.' + mdl, lib)
    module.setup(client)


def run(token: str):
    client.run(token)
