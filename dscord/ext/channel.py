from typing import Union

import discord
from discord.ext import commands

from dscord.func import clamp, randoms

AnyChannel = Union[
    discord.CategoryChannel, 
    discord.VoiceChannel, 
    discord.StageChannel, 
    discord.TextChannel
]


class Channel(commands.Cog):
    @commands.command('ccat', brief='Create category channel')
    async def create_category_channel(
        self, ctx, *, name: str = randoms()
    ) -> None:
        await ctx.guild.create_category_channel(name)
 
    @commands.command('cstg', brief='Create stage channel')
    async def create_stage_channel(
        self, ctx, *, name: str = randoms()
    ) -> None:
        await ctx.guild.create_stage_channel(name)
   
    @commands.command('ctxt', brief='Create text channel')
    async def create_text_channel(
        self, ctx, *, name: str = randoms()
    ) -> None:
        await ctx.guild.create_text_channel(name)

    @commands.command('cvo', brief='Create voice channel')
    async def create_voice_channel(
        self, ctx, name: str = randoms()
    ) -> None:
        await ctx.guild.create_voice_channel(name)

    @commands.command('ctxts', brief='Create text channels')
    async def create_text_channels(
        self, ctx, count: int, *, name: str = None
    ) -> None:
        if name is None: 
            name = randoms()
        category = await ctx.guild.create_category_channel(name)
        count = clamp(count, min_i=1, max_i=50)
        for i in range(count):
            if name is None:
                name = randoms()
            else:
                name += f'-{i}'
            await category.create_text_channel(name)

    @commands.command('cdel', brief='Delete channel')
    async def delete_any_channel(
        self, ctx, channel: AnyChannel = None
    ) -> None:
        if channel is None:
            channel = ctx.channel
        elif channel is discord.CategoryChannel:
            for c in channel.channels: 
                await c.delete()
        await channel.delete()


def setup(bot):
    bot.add_cog(Channel())
