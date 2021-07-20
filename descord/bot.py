import importlib
from discord.ext import commands

client = commands.Bot(',')

@client.command('load')
async def load_command(ctx, mdl):
    load(mdl)
    await ctx.send(f'`{mdl}` loaded')

def load(mdl, lib='descord.ext'):
    module = importlib.import_module('.'+mdl, lib)
    module.setup(client)

def run(token):
    client.run(token)
