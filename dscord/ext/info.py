from discord import Member, Role
from discord.ext import commands

from dscord.ext import channel
from dscord.func import dict_wrap

attrChn = ['category', 'created_at', 'guild', 'name', 'permissions_synced', 'position']
attrRole = ['color', 'created_at', 'guild', 'hoist', 'id', 'managed', 'mentionable', 'permissions', 'position', 'tags']
attrUsr = ['activities', 'activity', 'avatar', 'avatar_url', 'bot', 'color', 'created_at', 'default_avatar', 'default_avatar_url', 'desktop_status', 'discriminator', 'display_name', 'dm_channel', 'guild', 'guild_permissions', 'id', 'joined_at', 'mention', 'mobile_status', 'mutual_guilds', 'name', 'nick', 'pending', 'premium_since', 'public_flags', 'raw_status', 'relationship', 'roles', 'status', 'system', 'top_role', 'voice', 'web_status']


class Info(commands.Cog):
    @commands.command('schn', brief='Get chn info')
    async def spyChannel(self, ctx, channel: channel.AnyChannel = None) -> None:
        if not channel: channel = ctx.channel
        for log in dict_wrap(channel, attrChn):
            await ctx.send(log)

    @commands.command('smem', brief='You stalker')
    async def spyMember(self, ctx, member: Member = None) -> None:
        if not member: member = ctx.author
        for log in dict_wrap(member, attrUsr):
            await ctx.send(log)

    @commands.command('srole', brief='Get role info')
    async def spyRole(self, ctx, role: Role) -> None:
        for log in dict_wrap(role, attrRole):
            await ctx.send(log)


def setup(bot):
    bot.add_cog(Info())
