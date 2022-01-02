from contextlib import contextmanager
import importlib
import inspect
import os
import sys
from typing import List, Literal, Tuple

from discord.ext import commands
from discord.ext.commands import CommandNotFound, CheckFailure, CommandRegistrationError
import requests

from blurpo.func import (
    basename, database, error_log, repo_check, 
    send_embed, subprocess_log, try_log, wrap
)


def prefix(d: str) -> None:
    global client
    client = commands.Bot(d)


prefix(',')


def run() -> None:
    with database() as db:
        ls, rs = reld_scope()
        ls and print(f'{", ".join(ls)} loaded')
        rs and print(f'{", ".join(rs)} loaded')
    client.run(os.environ['TOKEN'])


@contextmanager
def try_unload(chn_id: int) -> None:
    try:
        yield
    except Exception as e:
        if isinstance(e, KeyError):
            e = Exception('Ext not found')
        error_log(e, chn_id)


# Add, remove or get extension entries from database
def add_scope(scope: Literal['local', 'remote'], value: str) -> None:
    with database() as db:
        scopes = db['Extension']
        if value not in scopes[scope]:
            scopes[scope].append(value)
            scopes[scope].sort()
            db['Extension'] = scopes


def rmv_scope(scope: Literal['local', 'remote'], value: str) -> None:
    with database() as db:
        scopes = db['Extension']
        if value in scopes[scope]:
            scopes[scope].remove(value)
            db['Extension'] = scopes


def get_scope(scope: Literal['local', 'remote'], channel_id: int) -> None:
    with database() as db:
        scopes = db['Extension']
        scopes = scopes[scope]
        log = '\n'.join(scopes) or 'None'
        print(log)
        send_embed(channel_id, [log], title=scope.capitalize())


def lazy_ext(f: callable) -> callable:
    def auf(x: str) -> None:
        f('.' in x and x or 'blurpo.ext.' + x)
    return auf


# Load or unload extension from local or remote
@lazy_ext
def load_ext(ext: str) -> None:
    i = ext.rfind('.')
    module = importlib.import_module(ext[i:], ext[:i])
    module.setup(client)


@lazy_ext
def unld_ext(ext: str) -> None:
    for name, obj in inspect.getmembers(sys.modules[ext]):
        if inspect.isclass(obj): 
            issubclass(obj, commands.Cog) and client.remove_cog(name)


def load_url(url: str) -> int:
    req = requests.get(url)
    if req.status_code == 200:
        name = basename(url)
        open(f'exts/{name}.py', 'w').write(req.text)
        load_ext(name, 'exts')
    return req.status_code


def unld_url(url: str) -> None:
    name = basename(url)
    unld_ext(f'exts.{name}')
    os.remove(f'exts/{name}.py')


def reld_scope(chn_id: int = None) -> Tuple[List[str], List[str]]:
    with database() as db:
        scopes = db['Extension']
        ls, rs = [], []
        for ext in scopes['local']:
            with try_log(chn_id):
                load_ext(ext)
                ls.append(ext)
        for url in scopes['remote']:
            with try_log(chn_id):
                load_url(url)
                rs.append(url)
        return ls, rs


@client.event
async def on_ready() -> None:
    print('Authorized.')


@client.event
async def on_command_error(ctx, e) -> None:
    if not isinstance(e, (CommandNotFound, CheckFailure)):
        error_log(e, ctx.channel.id)


@client.command()
async def restart(ctx) -> None:
    await ctx.send('Restarting')
    os.execl(sys.executable, sys.executable, *sys.argv)


@client.command()
async def update(ctx) -> None:
    await ctx.send('Updating')
    os.system('pip install git+https://github.com/thisgary/blurpo')
    await ctx.invoke(client.get_command('restart'))


@client.command('pip')
async def pip_cmd(ctx, mode: str, package: str) -> None:
    if mode not in ['i', 'u']:
        raise Exception('Invalid mode. (only "i" or "u")')
    action = 'install' if mode == 'i' else 'uninstall'
    log, t = subprocess_log(['pip', action, package])
    send_embed(
        ctx.channel.id, wrap(log, lang='bash'), title='Output',
        footer={'text': f'Runtime: {t}s'}
    )


@client.command('exts', brief='List exts')
async def get_exts_cmd(ctx) -> None:
    get_scope('local', ctx.channel.id)


@client.command('urls', brief='List urls')
async def get_urls_cmd(ctx) -> None:
    get_scope('remote', ctx.channel.id)


@client.command('load', brief='Load local exts')
async def load_exts_cmd(ctx, *exts: str) -> None:
    for ext in exts:
        with try_log(ctx.channel.id):
            load_ext(ext)
            add_scope('local', ext)
    get_scope('local', ctx.channel.id)


@client.command('unld', brief='Unload local exts')
async def unld_exts_cmd(ctx, *exts: str) -> None:
    for ext in exts:
        with try_unload(ctx.channel.id):
            rmv_scope('local', ext)
            unld_ext(ext)
    get_scope('local', ctx.channel.id)


@client.command('loadurl', brief='Load remote exts')
async def load_urls_cmd(ctx, *urls: str) -> None:
    for url in urls:
        with try_log(ctx.channel.id):
            url = repo_check(url)
            load_url(url)
            add_scope('remote', url)
    get_scope('remote', ctx.channel.id)


@client.command('unldurl', brief='Unload remote exts')
async def unld_urls_cmd(ctx, *urls: str) -> None:
    for url in urls:
        with try_unload(ctx.channel.id):
            rmv_scope('remote', url)
            unld_url(url)
    get_scope('remote', ctx.channel.id)


@client.command('reld', brief='Reload exts')
async def reld_scope_cmd(ctx) -> None:
    log = ['\n'.join(s) for s in reld_scope(ctx.channel.id)]
    send_embed(ctx.channel.id, log, title='Reloaded')
