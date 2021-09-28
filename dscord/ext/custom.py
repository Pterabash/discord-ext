from urllib.request import urlopen

from discord import Game, Member, Status
from discord.ext import commands


class Customize(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command('become', brief='D-D-D-Decade')
    async def custImposter(self, ctx, member: Member = None) -> None:
        if not member: member = ctx.author
        avatar = await member.avatar_url.read()
        await self.bot.user.edit(username=member.name, avatar=avatar)
        await ctx.send(f'Hi, I am {member.name}')

    @commands.command('name', brief='Rename bot')
    async def custName(self, ctx, *, name: str) -> None:
        await self.bot.user.edit(username=name)

    @commands.command('pfp', brief='Change bot pfp')
    async def custPfp(self, ctx, url: str = None) -> None:
        avatar = (
            ctx.message.attachments[0].read() if ctx.message.attachments
            else urlopen(url).read() 
        )
        await self.bot.user.edit(avatar=avatar)

    @commands.command('status', brief='Change bot status')
    async def custStatus(self, ctx, status: Status, *, activity: str) -> None:
        game = Game(activity)
        await self.bot.change_presence(status=status, activity=game)


def setup(bot):
    bot.add_cog(Customize(bot))
