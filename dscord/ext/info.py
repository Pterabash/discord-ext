from discord import Member, Role
from discord.ext import commands

from dscord.ext import channel

from dscord.func import list_attrs, send_embed


channel_attr = [
    'category', 'created_at', 'guild', 'name', 'permissions_synced',
    'position'
]
role_attr = [
    'color', 'created_at', 'guild', 'hoist', 'id', 'managed',
    'mentionable', 'permissions', 'position', 'tags'
]
member_attr = [
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
        self, ctx, channel: channel.AnyChannel = None
    ) -> None:
        text = list_attrs(channel, channel_attr)
        send_embed(text, title='Channel Info')


    @commands.command('imem', brief='You stalker')
    async def get_member_info(self, ctx, member: Member = None) -> None:
        if not member: member = ctx.author
        send_embed(list_attrs(member, member_attr))

    @commands.command('irole', brief='Get role info')
    async def get_role_info(self, ctx, role: Role) -> None:
        send_embed(list_attrs(role, role_attr))


def setup(bot):
    bot.add_cog(Info())
