import discord
from discord.ext import commands
import requests


class Customize(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command('become', brief='D-D-D-Decade')
    async def custImposter(self, ctx, member: discord.Member = None) -> None:
        if not member: member = ctx.author
        avatar = await member.avatar_url.read()
        await self.bot.user.edit(username=member.name, avatar=avatar)
        await ctx.send(f'Hi, I am {member.name}')

    @commands.command('name', brief='Rename bot')
    async def custName(self, ctx, *, name: str) -> None:
        await self.bot.user.edit(username=name)

    @commands.command('pfp', brief='Change bot pfp')
    async def custPfp(self, ctx, url: str = None) -> None:
        if ctx.message.attachments:
            url = ctx.message.attachments[0].url
        avatar = requests.get(url).content
        await self.bot.user.edit(avatar=avatar)
    
    @commands.command('orca')
    async def custOrca(self, ctx) -> None:
        url = 'https://raw.githubusercontent.com/thisgary/dscord/main/asset/orca.jpg'
        await self.bot.user.edit(username='Orcinus', avatar=requests.get(url).content)

    @commands.command('status', brief='Change bot status')
    async def custStatus(self, ctx, status: discord.Status) -> None:
        await self.bot.change_presence(status=status)
    
    @commands.command('agame', brief='Playing __')
    async def custPlay(self, ctx, *, name: str) -> None:
        game = discord.Game(name)
        await self.bot.change_presence(activity=game)

    @commands.command('astream', brief='Streaming __')
    async def custStream(self, ctx, url: str, *, name: str) -> None:
        stream = discord.Streaming(name=name, url=url)
        await self.bot.change_presence(activity=stream)

    @commands.command('asong', brief='Listening __')
    async def custListen(self, ctx, *, name: str) -> None:
        song = discord.Activity(type=discord.ActivityType.listening, name=name)
        await self.bot.change_presence(activity=song)

    @commands.command('avid', brief='Watching __')
    async def custWatch(self, ctx, *, name: str) -> None:
        video = discord.Activity(type=discord.ActivityType.watching, name=name)
        await self.bot.change_presence(activity=video)


def setup(bot):
    bot.add_cog(Customize(bot))
