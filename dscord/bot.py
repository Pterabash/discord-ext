from importlib import import_module
from pydoc import render_doc, plaintext

from discord.ext import commands

from dscord import ext
from .func import code_wrap

client = commands.Bot(',')


@client.command('exthelp')
async def exthelp_command(ctx):
    ext_doc = render_doc(ext, 'Help on %s', renderer=plaintext)
    for x in code_wrap(ext_doc): await ctx.send(x)


@client.command('load')
async def load_command(ctx, mdl):
    load(mdl)
    await ctx.send(f'`{mdl}` loaded')


def load(mdl, lib='dscord.ext'):
    module = import_module('.' + mdl, lib)
    module.setup(client)


def run(token):
    client.run(token)
