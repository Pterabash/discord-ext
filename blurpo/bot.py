from importlib import import_module
import inspect
import logging
import os
from pathlib import Path
import sys

from discord.ext import commands
from discord.ext.commands import CommandNotFound, CheckFailure, CommandRegistrationError

from blurpo.func import basename, error_log, send_embeds, subprocess_log, wrap
from blurpo.fdict import fdict
from blurpo.urlimp import import_url


# Initialization
client = commands.Bot(',')
exts = fdict(local=set(), remote=set())


def prefix(d: str) -> None:
    global client
    client = commands.Bot(d)


def run() -> None:
    reld_exts()
    client.run(os.environ['TOKEN'])


# Internal functions
def __reflect(name: str) -> callable:
    return globals()[name]


def __predict(path: str) -> str:
    scope = 'local'
    # path like string
    if '/' in path:
        # local path
        if Path(path).exists():
            path = path.split('.')[0].replace('/', '.')
        # repo path
        elif not path.startswith('https://'):
            path = f'https://raw.githubusercontent.com/{path}'
            scope = 'remote'
    elif '.' not in path:
        # default module
        path = f'blurpo.ext.{path}'
    return path, scope


# Load or unload ext
def load_local(ext: str) -> None:
    i = ext.rfind('.')
    module = (import_module(ext) if i < 0 else 
              import_module(ext[i:], ext[:i]))
    module.setup(client)


def unld_local(ext: str) -> None:
    for name, obj in inspect.getmembers(sys.modules[ext]):
        if inspect.isclass(obj):
            issubclass(obj, commands.Cog) and client.remove_cog(name)


def load_remote(url: str) -> None:
    module = import_url(url)
    module.setup(client)


def unld_remote(url: str) -> None:
    name = basename(url)
    unld_local(f'mdl.{name}')
    os.remove(f'mdl/{name}.py')


def get_exts(chn_id: int, scope: str) -> None:
    paths = exts[scope]
    logging.info(f'Extensions: {exts}')
    d = ', ' if scope == 'local' else '/n'
    embed = wrap(d.join(paths) or 'None')
    send_embeds(chn_id, embed, title=scope.capitalize())


def reld_exts(chn_id: int = None) -> None:
    for scope in ['local', 'remote']:
        load_scope = __reflect(f'load_{scope}')
        for path in exts[scope]: 
            try:
                load_scope(path)
            except CommandRegistrationError:
                unld_local(path)
                load_scope(path)
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
    send_embeds(
        ctx.channel.id, wrap(log, lang='bash'), title='Output',
        footer={'text': f'Runtime: {t}s'}
    )


# Ext related commands
@client.command('exts', brief='Get exts')
async def get_exts_cmd(ctx) -> None:
    chn_id = ctx.channel.id
    get_exts(chn_id, 'local')
    get_exts(chn_id, 'remote')


@client.command('load', brief='Load exts')
async def load_locals_cmd(ctx, *paths: str) -> None:
    chn_id = ctx.channel.id
    for path in paths:
        try:
            path, scope = __predict(path)
            f_load = __reflect(f'load_{scope}')
            f_load(path)
            exts[scope].add(path)
        except CommandRegistrationError:
            unld_local(path)
            f_load(path)
        except ModuleNotFoundError:
            raise Exception('Extension not found')
        except Exception as e:
            error_log(e, chn_id)
    exts.write()
    get_exts(chn_id, scope)


@client.command('unld', brief='Unload exts')
async def unld_locals_cmd(ctx, *paths: str) -> None:
    chn_id = ctx.channel.id
    for path in paths:
        try:
            path, scope = __predict(path)
            exts[scope].discard(path)
            f_load = __reflect(f'unld_{scope}')
            f_load(path)
        except KeyError:
            raise Exception('Extension not found')
        except Exception as e:
            error_log(e, chn_id)
    exts.write()
    get_exts(chn_id, scope)


@client.command('reld', brief='Reload exts')
async def reld_scope_cmd(ctx) -> None:
    reld_exts(ctx.channel.id)
    get_exts(ctx.channel.id)
