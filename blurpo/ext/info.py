import logging

from discord import Guild, Member, Role
from discord.ext import commands

from blurpo.ext import channel
from blurpo.func import wrap, list_attrs, send_embeds

GLD_ATTR = [
    'afk_channel', 'afk_timeout', 'banner', 'banner_url', 'bitrate_limit', 
    'chunked', 'emoji_limit', 'explicit_content_filter', 'features', 
    'filesize_limit', 'icon', 'icon_url', 'id', 'large', 'max_members', 
    'max_presences', 'max_video_channel_users', 'me', 'member_count', 
    'mfa_level', 'name', 'owner', 'owner_id', 'preferred_locale', 
    'premium_subscriber_role','premium_subscription_count', 'premium_tier',
    'region', 'roles', 'self_role', 'splash', 'splash_url', 
    'unavailable', 'verification_level', 'voice_client'
]
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
    @commands.command('igld', brief='Get guild info')
    async def get_guild_info(
            self, ctx, *, guild: Guild = None) -> None:
        if not guild:
            guild = ctx.guild
        text = list_attrs(guild, GLD_ATTR)
        send_embeds(ctx.channel.id, wrap(text), title='Guild Info')

    @commands.command('ichn', brief='Get channel info')
    async def get_channel_info(
            self, ctx, *, channel: channel.AnyChannel = None) -> None:
        if not channel:
            channel = ctx.channel
        text = list_attrs(channel, CHN_ATTR)
        send_embeds(ctx.channel.id, wrap(text), title='Channel Info')

    @commands.command('imem', brief='You stalker')
    async def get_member_info(self, ctx, *, member: Member = None) -> None:
        if not member:
            member = ctx.author
        text = list_attrs(member, MEM_ATTR)
        send_embeds(ctx.channel.id, wrap(text), title='Member Info')

    @commands.command('irole', brief='Get role info')
    async def get_role_info(self, ctx, *, role: Role) -> None:
        text = list_attrs(role, ROLE_ATTR)
        send_embeds(ctx.channel.id, wrap(text), title='Member Info')


def setup(bot):
    bot.add_cog(Info())
