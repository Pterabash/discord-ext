from discord import Activity, ActivityType, Game, Member, Status, Streaming
from discord.ext import commands
import requests


class Customize(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command('name', brief='Set bot name')
    async def set_name(self, ctx, *, name: str) -> None:
        await self.bot.user.edit(username=name)

    @commands.command('pfp', brief='Set bot pfp')
    async def set_avatar(self, ctx, url: str = None) -> None:
        if ctx.message.attachments:
            url = ctx.message.attachments[0].url
        avatar = requests.get(url).content
        await self.bot.user.edit(avatar=avatar)

    @commands.command(
        'copy', brief='Mimic another member', 
        aliases=['become','henshin', 'morph', 'mimic', 'steal'])
    async def copy_member(self, ctx, member: Member = None) -> None:
        if member is None:
            member = ctx.author
        name = member.name
        avatar = member.avatar_url.read()
        await self.bot.user.edit(username=name, avatar=avatar)
        await ctx.send(f'Hi, I am {name}')

    @commands.command('status', brief='Change bot status')
    async def set_status(self, ctx, status: Status) -> None:
        await self.bot.change_presence(status=status)
    
    @commands.command('play', brief='Playing __')
    async def set_activity_game(self, ctx, *, name: str) -> None:
        game = Game(name)
        await self.bot.change_presence(activity=game)

    @commands.command('stream', brief='Streaming __')
    async def set_activity_stream(
            self, ctx, url: str, *, name: str) -> None:
        stream = Streaming(name=name, url=url)
        await self.bot.change_presence(activity=stream)

    @commands.command('listen', brief='Listening __')
    async def set_activity_listen(self, ctx, *, name: str) -> None:
        listen = Activity(type=ActivityType.listening, name=name)
        await self.bot.change_presence(activity=listen)

    @commands.command('watch', brief='Watching __')
    async def set_activity_watch(self, ctx, *, name: str) -> None:
        watch = Activity(type=ActivityType.watching, name=name)
        await self.bot.change_presence(activity=watch)


def setup(bot):
    bot.add_cog(Customize(bot))
