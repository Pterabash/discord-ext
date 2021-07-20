import importlib
import descord.ext
from descord.func import code_wrap
from discord.ext import commands

client = commands.Bot(',')

@client.command('exthelp')
async def exthelp_command(ctx):
    for x in code_wrap(help(descord.ext)): await ctx.send(x)

@client.command('load')
async def load_command(ctx, mdl):
    load(mdl)
    await ctx.send(f'`{mdl}` loaded')

def load(mdl, lib='descord.ext'):
    module = importlib.import_module('.'+mdl, lib)
    module.setup(client)

def run(token):
    client.run(token)
