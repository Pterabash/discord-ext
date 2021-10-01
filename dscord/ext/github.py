import os
from typing import Tuple
from urllib.request import urlopen

from discord.ext import commands
from dscord.func import database, send_embed


with database() as db:
    if 'Github' not in db:
        db['Github'] = {}


def basename(path: str) -> Tuple[str, str]:
    # Get file's basename from url
    # eg. https://website.com/index.html -> (index.html, index)
    return (base := path.split('/')[-1]), base.split('.')[0]


def extList(channel_id: int) -> None:
    with database() as db:
        exts = list(db['Github'])
        print(exts)
        send_embed(channel_id, '\n'.join(exts), title='Github Extensions')


def extLoad(bot: commands.Bot, path: str) -> None:
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


def extsLoad() -> None:
    with database() as db:
        exts = db['Github']
        for ext in exts.keys():
            try:
                extLoad(exts[ext])
            except Exception as e:
                print(e)


class Github(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command('gload', brief='Load exts. Path: [owner/repo/branch/filepath]')
    async def ghExtLoad(self, ctx, *paths: str) -> None:
        with database() as db:
            for path in paths:
                extLoad(self.bot, path)
                _, ext = basename(path)
                exts = db['Github'] # Blame shelve
                exts[ext] = path
                db['Github'] = exts
        extList(ctx.channel.id)

    @commands.command('gexts', brief='List exts')
    async def ghExtList(self, ctx) -> None:
        extList(ctx.channel.id)

    @commands.command('gunld', brief='Unload exts')
    async def ghExtsUnload(self, ctx, *exts: str) -> None:
        with database() as db:
            for ext in exts:
                es = db['Github'] # Blame shelve
                if ext in es:
                    del es[ext]
                db['Github'] = es
                self.bot.unload_extension(ext)
        extList(ctx.channel.id)

    @commands.command('greld', brief='Reload all exts')
    async def ghExtsReload(self, ctx) -> None:
        extsLoad()
        await ctx.send('Finished reloading')

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        extsLoad()


def setup(bot):
    bot.add_cog(Github(bot))
