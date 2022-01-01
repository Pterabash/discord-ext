import importlib
import inspect
import logging
import os
import sys
from typing import List, Literal

from discord.ext import commands
from discord.ext.commands import CommandNotFound, CheckFailure
import requests

from blurpo.func import basename, database, error_log, send_embed, wrap


def prefix(d: str) -> None:
    global client
    client = commands.Bot(d)


prefix(',')


def run() -> None:
    with database() as db:
        if 'Extension' in db:
            loads = reld_exts()
            loads and print(f'{", ".join(loads)} loaded')
        else:
            db['Extension'] = {'local': [], 'remote': []}
    client.run(os.environ['TOKEN'])


# Add, remove or get extension entries from database
def add_scope(scope: Literal['local', 'remote'], value: str) -> None:
    with database() as db:
        scopes = db['Extension'][scope]
        if value not in scopes:
            scopes.append(value)
            db['Extension'][scope] = scopes


def rmv_scope(scope: Literal['local', 'remote'], value: str) -> None:
    with database() as db:
        scopes = db['Extension'][scope]
        if value in scopes:
            scopes.remove(value)
            db['Extension'][scope] = scopes


def get_scope(scope: Literal['local', 'remote'], channel_id: int) -> None:
    with database() as db:
        scopes = db['Extension'][scope]
        log = '\n'.join(scopes) or 'None'
        print(log)
        send_embed(channel_id, [log], title=scope.capitalize())


# Load or unload extension from local or remote
def load_ext(ext: str) -> None:
    i = ext.rfind('.')
    module = importlib.import_module(ext[i:], ext[:i])
    module.setup(client)
    add_scope('local', ext)


def load_url(url: str) -> None:
    req = requests.get(url)
    if req.status_code == 200:
        name = basename(url)
        open(f'exts/{name}.py', 'w').write(req.text)
        load_ext(f'exts.{name}')
        add_scope('remote', url)


def unld_ext(ext: str) -> None:
    rmv_scope('local', ext)
    for name, obj in inspect.getmembers(sys.modules[ext]):
        if inspect.isclass(obj): 
            issubclass(obj, commands.Cog) and client.remove_cog(name)


def unld_url(url: str) -> None:
    rmv_scope('remote', url)
    name = basename(url)
    unld_ext(f'exts.{name}')
    os.remove(f'exts/{name}.py')


def reld_exts() -> List[str]:
    with database() as db:
        exts = db['Extension']['local']
        loads = []
        for ext in exts:
            try:
                load_ext(ext)
                loads.append(ext)
            except:
                logging.exception('message')
        return loads


@client.event
async def on_ready() -> None:
    print('Authorized.')


@client.event
async def on_command_error(ctx, e) -> None:
    if not isinstance(e, (CommandNotFound, CheckFailure)):
        error_log(e, ctx.channel.id)


@client.command()
async def update(ctx) -> None:
    await ctx.send('Updating')
    os.system('pip3 install git+https://github.com/thisgary/blurpo')
    await ctx.send('Restarting')
    os.execl(sys.executable, sys.executable, *sys.argv)


@client.command('exts', brief='List exts')
async def get_exts_cmd(ctx) -> None:
    get_scope('local', ctx.channel.id)


@client.command('urls', brief='List urls')
async def get_urls_cmd(ctx) -> None:
    get_scope('remote', ctx.channel.id)


@client.command('load', brief='Load local exts')
async def load_exts_cmd(ctx, *exts: str) -> None:
    for ext in exts:
        try:
            load_ext(ext)
        except Exception as e:
            error_log(e, ctx.channel.id)
    get_scope('local', ctx.channel.id)


@client.command('loadurl', brief='Load remote exts')
async def load_exts_cmd(ctx, *urls: str) -> None:
    for url in urls:
        try:
            load_url(url)
        except Exception as e:
            error_log(e, ctx.channel.id)
    get_scope('remote', ctx.channel.id)
    get_scope('local', ctx.channel.id)


@client.command('unld', brief='Unload exts')
async def unld_exts_cmd(ctx, *exts: str) -> None:
    for ext in exts:
        try:
            unld_ext(ext)
        except Exception as e:
            error_log(e, ctx.channel.id)
    get_scope('local', ctx.channel.id)


@client.command('unldurl', brief='Unload exts')
async def unld_exts_cmd(ctx, *urls: str) -> None:
    for url in urls:
        try:
            unld_ext(url)
        except Exception as e:
            error_log(e, ctx.channel.id)
    get_scope('remote', ctx.channel.id)
    get_scope('local', ctx.channel.id)


@client.command('reld', brief='Reload exts')
async def reld_exts_cmd(ctx) -> None:
    log = '\n'.join(reld_exts())
    send_embed(ctx.channel.id, wrap(log), title='Reloaded')


if not os.path.isdir('exts'):
    os.mkdir('exts')
