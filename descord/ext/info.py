import discord
from discord.ext import commands
from descord.func import ls_attr
from descord.cog import role, channel


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
            'getchn',
            brief='Get channel info')
    async def infoChn(self, ctx, chn:channel.chnAny=None):
        if not chn: chn = ctx.channel
        for l in ls_attr(chn, channel.chnAttr): await ctx.send(l)

    @commands.command(
            'getrole',
            brief='Get role information')
    async def infoRole(self, ctx, rl: discord.Role):
        for l in ls_attr(rl, role.roleAttr): await ctx.send(l)

    @commands.command(
            'getuser',
            brief='You stalker')
    async def infoMember(self, ctx, member:discord.Member=None):
        if not member: member = ctx.author
        for l in ls_attr(member): await ctx.send(l)


def setup(bot):
    bot.add_cog(Info(bot))
