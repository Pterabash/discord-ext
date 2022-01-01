from discord import Member, Role
from discord.ext import commands

from blurpo.ext import channel
from blurpo.func import list_attrs, send_embed


CHN_ATTR = [
    'category', 'created_at', 'guild', 'name', 
    'permissions_synced', 'position'
]
ROLE_ATTR = [
    'color', 'created_at', 'guild', 'hoist', 'id', 'managed',
    'mentionable', 'permissions', 'position', 'tags'
]
MEM_ATTR = [
    'activities', 'activity', 'avatar', 'avatar_url', 'bot', 'color', 
    'created_at', 'default_avatar', 'default_avatar_url', 'desktop_status', 
    'discriminator', 'display_name', 'dm_channel', 'guild',
    'guild_permissions', 'id', 'joined_at', 'mention', 'mobile_status', 
    'mutual_guilds', 'name', 'nick', 'pending', 'premium_since',
    'public_flags', 'raw_status', 'relationship', 'roles', 'status',
    'system', 'top_role', 'voice', 'web_status'
]


class Info(commands.Cog):
    @commands.command('ichn', brief='Get chn info')
    async def get_channel_info(
            self, ctx, channel: channel.AnyChannel = None) -> None:
        text = list_attrs(channel, CHN_ATTR)
        send_embed(ctx.channel.id, text, title='Channel Info')

    @commands.command('imem', brief='You stalker')
    async def get_member_info(self, ctx, member: Member = None) -> None:
        if not member: 
            member = ctx.author
        send_embed(ctx.channel.id, list_attrs(member, MEM_ATTR))

    @commands.command('irole', brief='Get role info')
    async def get_role_info(self, ctx, role: Role) -> None:
        send_embed(ctx.channel.id, list_attrs(role, ROLE_ATTR))


def setup(bot):
    bot.add_cog(Info())
