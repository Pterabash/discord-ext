import os
import sys
from typing import List, Tuple

from discord.ext import commands
import requests

from blurpo.func import database, error_log, send_embed, wrap


def prefix(d: str) -> None:
    global client
    client = commands.Bot(d)


prefix(',')


def url_check(url: str) -> str:
    if not url.startswith('https://'):
        url = 'https://raw.githubusercontent.com/' + url
    return url


def ext_path(url: str) -> Tuple[str, str]:
    path = 'ext/' + url.split('/')[-1]
    ext = path.split('.')[0].replace('/', '.')
    return path, ext


def load(url: str) -> None:
    req = requests.get(url_check(url))
    path, ext = ext_path(url) 
    if req.status_code == 200: 
        open(path, 'w').write(req.text)
        try: 
            client.load_extension(ext)
        except commands.ExtensionAlreadyLoaded: 
            client.reload_extension(ext)
    else:
        raise Exception(f'{url} {req.status_code}')


def reld_exts() -> List[str]:
    with database() as db:
        exts = db['Extensions']
        loads = []
        for ext in exts.keys():
            try:
                load(exts[ext])
                loads.append(ext)
            except Exception as e: 
                print(e)
    return exts


def list_exts(channel_id: int) -> None:
    with database() as db:
        exts = db['Extensions']
        ls = [f'**{e}**\n{exts[e]}' for e in list(exts)]
        send_embed(
            channel_id, ['\n'.join(ls)], 
            title='Loaded Extensions', color=333333, token='ODMwNzA1MjYyODY3MzgyMjcz.YHKkkA.z-ltZZrMfCpDbMC1JBebLZFLOxI'
        )


def run(token: str) -> None:
    if not os.path.isdir('ext'):
        os.mkdir('ext')
    with database() as db:
        if 'Extensions' in db:
            exts = reld_exts()
            if exts:
                print(f'{", ".join(exts)} loaded')
        else: 
            db['Extensions'] = {}
    client.run(token)


@client.command('load', brief='Load exts online')
async def load_exts_cmd(ctx, *urls: str) -> None:
    with database() as db:
        for u in urls:
            try:
                load(u)
                _, ext = ext_path(u)
                exts = db['Extensions']
                exts[ext] = url_check(u)
                db['Extensions'] = exts
            except Exception as e:
                error_log(e, ctx.channel.id)
    list_exts(ctx.channel.id)


@client.command('unld', brief='Unload exts')
async def unld_exts_cmd(ctx, *names: str) -> None:
    with database() as db:
        for n in names:
            try:
                if not n.startswith('exts.'):
                    n = 'exts.' + n
                exts = db['Extensions']
                if n in exts: 
                    del exts[n]
                db['Extensions'] = exts
            except Exception as e:
                error_log(e, ctx.channel.id)
            try:
                client.unload_extension(n)
            except Exception as e:
                error_log(e, ctx.channel.id) 
    list_exts(ctx.channel.id)


@client.command('exts', brief='List exts')
async def list_exts_cmd(ctx) -> None:
    list_exts(ctx.channel.id)


@client.command('greld', brief='Reload all exts')
async def reld_exts_cmd(ctx) -> None:
    exts = reld_exts()
    send_embed(
        ctx.channel.id, wrap('\n'.join(exts), code='bash'), 
        title='Extensions Reloaded', color=333333,
    )


@client.command()
async def update(ctx) -> None:
    await ctx.send('Updating')
    os.system('pip3 install git+https://github.com/thisgary/blurpo')
    await ctx.send('Restarting')
    os.execl(sys.executable, sys.executable, *sys.argv)


@client.event
async def on_ready() -> None:
    print('Bot is up!')


@client.event
async def on_command_error(ctx, e) -> None:
    if (isinstance(e, commands.CommandNotFound) 
        or isinstance(e, commands.CheckFailure)): return
    else:
        error_log(e, ctx.channel.id)
