import os
from typing import List
from urllib.request import urlretrieve

from discord.ext import commands
from dscord.func import Db, code_wrap

base_url = 'https://raw.githubusercontent.com/'
db = Db('path')


async def extlist(ctx) -> None:
    keys = db.keys()
    if keys:
        logs = code_wrap('\n'.join(keys))
        for log in logs: await ctx.send(log)
    else: await ctx.send('No extension loaded from Github')


def basename(path: str) -> str:
    base = path.split('/')[-1]
    name = base.split('.')[0]
    return base, name


def extLoad(bot: commands.Bot, path: str) -> None:
    base, name = basename(path)
    url = base_url + path
    urlretrieve(url, base)
    try: bot.load_extension(name)
    except commands.ExtensionAlreadyLoaded:
        bot.reload_extension(name)
    finally: os.remove(base)


def extsLoad() -> None:
    for path in db.keys():
        try: extLoad(path)
        except Exception as e: print(e)


class Github(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command('gload', brief='Path: [owner/repo/branch/filepath]')
    async def extsLoad(self, ctx, *paths: str) -> None:
        for path in paths:
            extLoad(self.bot, path)
            _, ext = basename(path)
            db.write(path, ext)
        await extlist(ctx)

    @commands.command('gexts', brief='List exts')
    async def extsList(self, ctx) -> None:
        await extlist(ctx)

    @commands.command('greld', brief='Reload all exts')
    async def extsReload(self, ctx) -> None:
        extsLoad()
        await ctx.send('Done')
    
    @commands.command('gunld', brief='Unload exts')
    async def extsUnload(self, ctx, *exts: str) -> None:
        for ext in exts:
            db.erase(str(ext))
            self.bot.unload_extension(ext)
        await extlist(ctx)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        extsLoad()


def setup(bot):
    bot.add_cog(Github(bot))
