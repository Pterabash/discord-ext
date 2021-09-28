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

    @commands.command('status', brief='Change bot status')
    async def custStatus(self, ctx, status: discord.Status) -> None:
        await self.bot.change_presence(status=status)
    
    @commands.command('play', brief='Activity: playing')
    async def custPlay(self, ctx, *, name: str) -> None:
        game = discord.Game(name)
        await self.bot.change_presence(status=self.bot.status, activity=game)

    @commands.command('stream', brief='Activity: streaming')
    async def custStream(self, ctx, url: str, *, name: str) -> None:
        stream = discord.Streaming(name, url=url)
        await self.bot.change_presence(status=self.bot.status, activity=stream)

    @commands.command('listen', brief='Activity: listening')
    async def custListen(self, ctx, url: str, *, name: str) -> None:
        song = discord.Activity(type=discord.ActivityType.listening, name=name)
        await self.bot.change_presence(status=self.bot.status, activity=song)

    @commands.command('watch', brief='Activity: watching')
    async def custWatch(self, ctx, url: str, *, name: str) -> None:
        video = discord.Activity(type=discord.ActivityType.watching, name=name)
        await self.bot.change_presence(status=self.bot.status, activity=video)


def setup(bot):
    bot.add_cog(Customize(bot))
