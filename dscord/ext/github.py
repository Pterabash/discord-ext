from discord.ext import commands

import os
from dscord.func import Db
from urllib.request import urlretrieve

paths = Db('path')
gh = 'https://raw.githubusercontent.com/'

def pathToExt(path):
    f = path.split('/')[-1]
    ext = f.split('.')[0]
    return f, ext

def extLoad(path):
    f, ext = pathToExt(path)
    urlretrieve(gh+path, f)
    try: bot.load_extension(ext)
    except commands.ExtensionAlreadyLoaded: bot.reload_extension(ext)
    finally: os.remove(f)

def extLoadAll():
    for path in paths.readkey():
        try: extLoad(path)
        except Exception as e: print(e)


class GhExt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        extLoadAll()

    @commands.command(
            'rfsh',
            brief='Reload all extensions')
    async def ghRefresh(self, ctx):
        extLoadAll()
        await ctx.send('Reloaded')

    @commands.command(
            'load',
            brief='owner/repo/branch/file.py')
    async def ghLoad(self, ctx, *paths):
        for path in paths:
            extLoad(path)
            _, ext = pathToExt(path)
            paths.write(ext, path)
        await ctx.send(codelist(paths.readkey()))

    @commands.command('unload')
    async def ghUnload(self, ctx, *exts):
        for ext in exts:
            paths.erase(ext)
            bot.unload_extension(ext)


def setup(bot):
    bot.add_cog(GhExt(bot))
