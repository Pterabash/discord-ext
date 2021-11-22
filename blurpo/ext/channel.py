from typing import Union

from discord import CategoryChannel, VoiceChannel, StageChannel, TextChannel
from discord.ext import commands

from blurpo.func import randoms


AnyChannel = Union[CategoryChannel, VoiceChannel, StageChannel, TextChannel]


class Channel(commands.Cog):
    @commands.command('ccat', brief='Create category channel')
    async def create_category_channel(
            self, ctx, *, name: str = randoms()) -> None:
        await ctx.guild.create_category_channel(name)
 
    @commands.command('cstg', brief='Create stage channel')
    async def create_stage_channel(
            self, ctx, *, name: str = randoms()) -> None:
        await ctx.guild.create_stage_channel(name)
   
    @commands.command('ctxt', brief='Create text channel')
    async def create_text_channel(
            self, ctx, *, name: str = randoms()) -> None:
        await ctx.guild.create_text_channel(name)

    @commands.command('cvo', brief='Create voice channel')
    async def create_voice_channel(
            self, ctx, name: str = randoms()) -> None:
        await ctx.guild.create_voice_channel(name)

    @commands.command('cdel', brief='Delete channel')
    async def delete_any_channel(
            self, ctx, *channels: AnyChannel) -> None:
        if not channels:
            await ctx.channel.delete()
        for channel in channels:
            if channel is CategoryChannel:
                for c in channel.channels: 
                    await c.delete()
            await channel.delete()


def setup(bot): 
    bot.add_cog(Channel())
