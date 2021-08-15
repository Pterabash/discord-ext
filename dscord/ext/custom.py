from discord import Game, Member, Status
from discord.ext import commands


class Customize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Morph bot into member')
    async def morph(self, ctx, member: Member = None):
        if not member: member = ctx.author
        avatar = await member.avatar_url.read()
        await self.bot.user.edit(username=member.name, avatar=avatar)

    @commands.command(brief='Rename bot')
    async def rename(self, ctx, *, name: str):
        await self.bot.user.edit(username=name)

    @commands.command(brief='Change bot status')
    async def presence(self, ctx, status: Status, *, activity: str):
        game = Game(activity)
        await self.bot.change_presence(status=status, activity=game)


def setup(bot):
    bot.add_cog(Customize(bot))
