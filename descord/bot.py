import pydoc
import importlib
import descord.ext
from discord.ext import commands
from descord.func import code_wrap

client = commands.Bot(',')

@client.command('exthelp')
async def exthelp_command(ctx):
    ext_doc = pydoc.render_doc(descord.ext, 'Help on %s', renderer=pydoc.plaintext)
    for x in code_wrap(ext_doc): await ctx.send(x)

@client.command('load')
async def load_command(ctx, mdl):
    load(mdl)
    await ctx.send(f'`{mdl}` loaded')

def load(mdl, lib='descord.ext'):
    module = importlib.import_module('.'+mdl, lib)
    module.setup(client)

def run(token):
    client.run('x')
