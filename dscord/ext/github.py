import os
from urllib.request import urlretrieve

from discord.ext import commands

from dscord.func import Db, code_wrap

base_url = 'https://raw.githubusercontent.com/'
db = Db('path')


def basename(path: str) -> str:
    base = path.split('/')[-1]
    name = base.split('.')[0]
    return base, name


def extLoad(bot: commands.Bot, path: str):
    base, name = basename(path)
    url = base_url + path
    urlretrieve(url, base)
    try: bot.load_extension(name)
    except commands.ExtensionAlreadyLoaded:
        bot.reload_extension(name)
    finally: os.remove(base)


def extsLoad():
    for path in db.keys():
        try: extLoad(path)
        except Exception as e: print(e)


class GithubExt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        extsLoad()

    @commands.command('ghreld', brief='Reload all extensions')
    async def extsReload(self, ctx):
        extsLoad()
        await ctx.send('Done')

    @commands.command('ghload', brief='[owner/repo/branch/file.py]')
    async def extsLoad(self, ctx, *paths):
        for path in paths:
            extLoad(self.bot, path)
            _, name = basename(path)
            db.write(path, name)
        logs = code_wrap('\n'.join(db.keys()))
        for log in logs: await ctx.send(log)

    @commands.command('ghunld', brief='Unload extensions')
    async def extsUnload(self, ctx, *exts):
        for ext in exts:
            db.erase(str(ext))
            self.bot.unload_extension(ext)


def setup(bot):
    bot.add_cog(GithubExt(bot))
