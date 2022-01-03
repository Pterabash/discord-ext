import importlib
import inspect
import os
import sys

from discord.ext import commands
from discord.ext.commands import CommandNotFound, CheckFailure, CommandRegistrationError
import requests

from blurpo.func import (
    basename, error_log, EvalFile,
    send_embed, subprocess_log, wrap
)


GH = 'https://raw.githubusercontent.com/'
client = commands.Bot(',')
ext = EvalFile('exts')


def prefix(d: str) -> None:
    global client
    client = commands.Bot(d)


def run() -> None:
    reld_exts()
    client.run(os.environ['TOKEN'])


def repo_url(url: str) -> str:
    return url if '.' in url else 'https://raw.githubusercontent.com/' + url

# Load or unload ext
def load_ext(ext: str) -> None:
    ext = ext if '.' in ext else 'blurpo.ext.' + ext
    i = ext.rfind('.')
    module = importlib.import_module(ext[i:], ext[:i])
    module.setup(client)


def unld_ext(ext: str) -> None:
    ext = ext if '.' in ext else 'blurpo.ext.' + ext
    for name, obj in inspect.getmembers(sys.modules[ext]):
        if inspect.isclass(obj):
            issubclass(obj, commands.Cog) and client.remove_cog(name)


def load_url(url: str) -> int:
    url = url if url.startswith('https://') else GH + url
    req = requests.get(url)
    s = req.status_code
    if s != 200:
        raise Exception(f'Status code {s}')
    name = basename(url)
    open(f'exts/{name}.py', 'w').write(req.text)
    load_ext(f'exts.{name}')


def unld_url(url: str) -> None:
    url = url if url.startswith('https://') else GH + url
    name = basename(url)
    unld_ext(f'exts.{name}')
    os.remove(f'exts/{name}.py')


# Get or reload exts
def get_exts(channel_id: int) -> None:
    paths = ext.get(f=sorted)
    log = '\n'.join(paths) or 'None'
    print(log)
    send_embed(channel_id, [log], title='Extension')


def reld_exts(chn_id: int = None) -> None:
    for p in ext.get():
        try:
            load_url(p) if '/' in p else load_ext(p)
        except Exception as e:
            error_log(e, chn_id)


@client.event
async def on_ready() -> None:
    print('Authorized.')


@client.event
async def on_command_error(ctx, e) -> None:
    if not isinstance(e, (CommandNotFound, CheckFailure)):
        error_log(e, ctx.channel.id)


# System related commands
@client.command()
async def restart(ctx) -> None:
    await ctx.send('Restarting')
    os.execl(sys.executable, sys.executable, *sys.argv)


@client.command()
async def update(ctx) -> None:
    await ctx.send('Updating')
    os.system('pip install git+https://github.com/thisgary/blurple-o')
    await ctx.invoke(client.get_command('restart'))


@client.command('pip')
async def pip_cmd(ctx, mode: str, pkg: str) -> None:
    MODE = ['u', 'i']
    if mode not in MODE:
        raise Exception('Invalid mode. (i, u)')
    i = MODE.index(mode) * 2
    args = ['pip', 'uninstall'[i:], pkg]
    inp = b'y' if i < 1 else None
    log, t = subprocess_log(args, inp)
    send_embed(
        ctx.channel.id, wrap(log, lang='bash'), title='Output',
        footer={'text': f'Runtime: {t}s'}
    )


# Ext related commands
@client.command('exts', brief='Get exts')
async def get_exts_cmd(ctx) -> None:
    get_exts(ctx.channel.id)


@client.command('load', brief='Load exts')
async def load_exts_cmd(ctx, *paths: str) -> None:
    for p in paths:
        try:
            load_url(p) if '/' in p else load_ext(p)
            ext.add(p)
        except Exception as e:
            error_log(e, ctx.channel.id)
    get_exts(ctx.channel.id)


@client.command('unld', brief='Unload exts')
async def unld_exts_cmd(ctx, *paths: str) -> None:
    for p in paths:
        try:
            ext.discard(p)
            unld_url(p) if '/' in p else unld_ext(p)
        except Exception as e:
            error_log(e, ctx.channel.id)
    get_exts(ctx.channel.id)


@client.command('reld', brief='Reload exts')
async def reld_scope_cmd(ctx) -> None:
    reld_exts(ctx.channel.id)
    get_exts(ctx.channel.id)
