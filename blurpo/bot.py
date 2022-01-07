from importlib import import_module
import inspect
import os
from pathlib import Path
import sys
from typing import Iterable

from discord.ext import commands
from discord.ext.commands import CommandNotFound, CheckFailure, CommandRegistrationError

from blurpo.func import basename, error_log, send_embed, subprocess_log, wrap
from blurpo.fdict import fdict
from blurpo.urlimp import import_url


GH = 'https://raw.githubusercontent.com/'

client = commands.Bot(',')
exts = fdict(local=set(), remote=set())


def prefix(d: str) -> None:
    global client
    client = commands.Bot(d)


def run() -> None:
    reld_exts()
    client.run(os.environ['TOKEN'])


def __loads(xs: Iterable[str], f: callable, chn_id: int) -> None:
    for x in xs:
        try:
            f(x)
        except Exception as e:
            error_log(e, chn_id)


def __mode(path) -> str:
    scope = 'local'
    if '/' in path:
        if Path(path).exists(): # is local
            path = path.split('.')[0].replace('/', '.')
        elif not path.startswith('https://'):
            path = GH + path
            scope = 'remote'
    elif '.' not in path:
        path = f'blurpo.ext.{path}'
    return path, scope


# Load or unload ext
def load_local(ext: str) -> None:
    i = ext.rfind('.')
    module = import_module(ext[i:], ext[:i])
    module.setup(client) 


def load_remote(url: str) -> None:
    module = import_url(url)
    module.setup(client)


def unld_local(ext: str) -> None:
    for name, obj in inspect.getmembers(sys.modules[ext]):
        if inspect.isclass(obj):
            issubclass(obj, commands.Cog) and client.remove_cog(name)


def unld_remote(url: str) -> None:
    name = basename(url)
    unld_local(f'mdl.{name}')
    os.remove(f'mdl/{name}.py')


# Get or reload exts
def get_exts(channel_id: int) -> None:    
    log = '\n'.join(exts['local']) or 'None'
    print(log)
    send_embed(channel_id, [log], title='Extension')


def reld_exts(chn_id: int = None) -> None:
    __loads(exts['local'], load_local, chn_id)
    __loads(exts['remote'], load_remote, chn_id)


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
async def load_locals_cmd(ctx, *paths: str) -> None:
    for path in paths:
        try:
            path, scope = __mode(path)
            globals()[f'load_{scope}'](path)
            exts[scope].add(path)
            exts.write()
        except Exception as e:
            error_log(e, ctx.channel.id)
    exts.write()
    get_exts(ctx.channel.id)


@client.command('unld', brief='Unload exts')
async def unld_locals_cmd(ctx, *paths: str) -> None:
    for path in paths:
        try:
            path, scope = __mode(path)
            exts[scope].discard(path)
            globals()[f'unld_{scope}'](path)
        except Exception as e:
            error_log(e, ctx.channel.id)
    exts.write()
    get_exts(ctx.channel.id)

@client.command('reld', brief='Reload exts')
async def reld_scope_cmd(ctx) -> None:
    reld_exts(ctx.channel.id)
    get_exts(ctx.channel.id)
