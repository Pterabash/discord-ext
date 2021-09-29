from discord import Member, Role
from discord.ext import commands

from .channel import AnyChannel
from dscord.func import dict_wrap

attrChn = ['category', 'created_at', 'guild', 'name', 'permissions_synced', 'position']

attrRole = ['color', 'created_at', 'guild', 'hoist', 'id', 'managed', 'mentionable', 'permissions', 'position', 'tags']


class Episonage(commands.Cog):
    @commands.command('schn', brief='Get chn info')
    async def spyChannel(self, ctx, channel: AnyChannel = None) -> None:
        if not channel: channel = ctx.channel
        for log in dict_wrap(channel, attrChn): await ctx.send(log)

    @commands.command('smbr', brief='You stalker')
    async def spyMember(self, ctx, member: Member = None) -> None:
        if not member: member = ctx.author
        for log in dict_wrap(member): await ctx.send(log)

    @commands.command('srole', brief='Get role info')
    async def spyRole(self, ctx, role: Role) -> None:
        for log in dict_wrap(role, attrRole): await ctx.send(log)


def setup(bot):
    bot.add_cog(Episonage())
