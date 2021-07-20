import discord
from discord.ext import commands


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
            'morph',
            brief='Morph into member')
    async def custMorph(self, ctx, member:discord.Member=None):
        if not member: member = ctx.author
        av = await member.avatar_url.read()
        await self.bot.user.edit(username=member.name, avatar=av)

    @commands.command(
            'rename',
            brief='Change bot name')
    async def custRename(self, ctx, *, name):
        await self.bot.user.edit(username=name)

    @commands.command(
            'presence',
            brief='online, idle, dnd, invisible')
    async def custPresence(self, ctx, status:discord.Status, *, activity):
        game = discord.Game(activity)
        await self.bot.change_presence(status=status, activity=game)


def setup(bot):
    bot.add_cog(Custom(bot))
