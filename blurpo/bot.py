import os
import sys
from typing import List

from discord.ext import commands
from discord.ext.commands import CommandNotFound, CheckFailure
import requests

from blurpo.func import (
    database, def_url, error_log, ext_path, send_embed, wrap
)


def set_prefix(d: str) -> None:
    global client
    client = commands.Bot(d)


set_prefix(',')


def run() -> None:
    if not os.path.isdir('ext'):
        os.mkdir('ext')
    with database() as db:
        if 'Extensions' in db:
            exts = reld_exts()
            if exts:
                print(f'{", ".join(exts)} loaded')
        else:
            db['Extensions'] = {}
    client.run(os.environ['TOKEN'])


def list_exts(channel_id: int) -> None:
    with database() as db:
        exts = db['Extensions']
        ls = [exts[e] for e in list(exts)]
        print(['\n'.join(ls)])
        send_embed(
            channel_id, ['\n'.join(ls) or 'None'],
            title='Extensions', color=333333
        )


def load_ext(url: str) -> None:
    req = requests.get(def_url(url))
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
                load_ext(exts[ext])
                loads.append(ext)
            except Exception as e:
                print(e)
    return exts


@client.event
async def on_ready() -> None:
    print('Bot is up!')


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
async def list_exts_cmd(ctx) -> None:
    list_exts(ctx.channel.id)


@client.command('load', brief='Load exts from net')
async def load_exts_cmd(ctx, *urls: str) -> None:
    with database() as db:
        for u in urls:
            try:
                load_ext(u)
                _, ext = ext_path(u)
                exts = db['Extensions']
                exts[ext] = def_url(u)
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


@client.command('reld', brief='Reload exts')
async def reld_exts_cmd(ctx) -> None:
    exts = reld_exts()
    send_embed(
        ctx.channel.id, wrap('\n'.join(exts), lang='bash'),
        title='Extensions Reloaded', color=333333,
    )
