import os
from typing import List, Tuple
from urllib.request import urlopen

from discord.ext import commands

from dscord.func import database, send_embed, wrap


def basename(path: str) -> Tuple[str, str]:
    # Get file's basename from url
    # eg. https://website.com/index.html -> (index.html, index)
    return (base := path.split('/')[-1]), base.split('.')[0]


def exts_list(chn_id: int) -> None:
    with database() as db:
        exts = list(db['Github'])
        text = wrap('\n'.join(exts), lang='bash')
        send_embed(
            chn_id, text, title='Github Extensions',
            color=333333
        )


def ext_load(bot: commands.Bot, path: str) -> None:
    base, name = basename(path)
    url = 'https://raw.githubusercontent.com/' + path
    with open(base, 'w') as f:
        f.write(urlopen(url).read().decode('utf-8'))
    try:
        bot.load_extension(name)
    except commands.ExtensionAlreadyLoaded:
        bot.reload_extension(name)
    finally:
        os.remove(base)


def exts_load(bot) -> List[str]:
    with database() as db:
        exts = db['Github']
        loaded = []
        for ext in exts.keys():
            try:
                ext_load(bot, exts[ext])
                loaded.append(ext)
            except Exception as e:
                print(e)
        return loaded


class Github(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        with database() as db:
            if 'Github' in db:
                exts = exts_load(self.bot)
                print(f'{exts} loaded')
            else:
                db['Github'] = {}

    @commands.command(
        'gload', brief='Load exts. Path: [owner/repo/branch/filepath]'
    )
    async def exts_load(self, ctx, *paths: str) -> None:
        with database() as db:
            for path in paths:
                ext_load(self.bot, path)
                _, ext = basename(path)
                exts = db['Github']
                exts[ext] = path
                db['Github'] = exts
        exts_list(ctx.channel.id)

    @commands.command('gunld', brief='Unload exts')
    async def exts_unload(self, ctx, *exts: str) -> None:
        with database() as db:
            for ext in exts:
                es = db['Github']
                if ext in es:
                    del es[ext]
                db['Github'] = es
                self.bot.unload_extension(ext)
        exts_list(ctx.channel.id)

    @commands.command('gexts', brief='List exts')
    async def exts_list(self, ctx) -> None:
        exts_list(ctx.channel.id)

    @commands.command('greld', brief='Reload all exts')
    async def ghExtsReload(self, ctx) -> None:
        exts = exts_load(self.bot)
        text = wrap('\n'.join(exts), lang='bash')
        send_embed(
            ctx.channel.id, text, title='Extensions Reloaded', 
            color=333333
        )


def setup(bot):
    bot.add_cog(Github(bot))