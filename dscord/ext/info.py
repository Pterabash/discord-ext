from discord import Member, Role
from discord.ext import commands

from .channel import AnyChannel
from dscord.func import dict_wrap

attrChn = ['category', 'created_at', 'guild', 'name', 'permissions_synced', 'position']

attrRole = ['color', 'created_at', 'guild', 'hoist', 'id', 'managed', 'mentionable', 'permissions', 'position', 'tags']


class Information(commands.Cog):
    @commands.command('getchn', brief='Get chn info')
    async def getChannel(self, ctx, channel: AnyChannel = None):
        if not channel: channel = ctx.channel
        for log in dict_wrap(channel, attrChn): await ctx.send(log)

    @commands.command('getmem', brief='You stalker')
    async def getMember(self, ctx, member: Member = None):
        if not member: member = ctx.author
        for log in dict_wrap(member): await ctx.send(log)

    @commands.command('getrole', brief='Get role info')
    async def getRole(self, ctx, role: Role):
        for log in dict_wrap(role, attrRole): await ctx.send(log)


def setup(bot):
    bot.add_cog(Information())
