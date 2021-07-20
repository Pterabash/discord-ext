import typing
import discord
from discord.ext import commands
from descord.func import clamp, rnd_str

chnAny = typing.Union[
        discord.StageChannel,
        discord.CategoryChannel,
        discord.VoiceChannel,
        discord.TextChannel]

chnAttr = [
        'category',
        'created_at',
        'guild',
        'name',
        'permissions_synced',
        'position']


class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
            'ctxt',
            brief='Create text channel')
    async def chnCreateText(self, ctx, name=rnd_str()):
        await ctx.guild.create_text_channel(name)
   
    @commands.command(
            'cvo',
            brief='Create voice channel')
    async def chnCreateVoice(self, ctx, name=rnd_str()):
        await ctx.guild.create_voice_channel(name)

    @commands.command(
            'ccat',
            brief='Create category "channel"')
    async def chnCreateCategory(self, ctx, name=rnd_str()):
        await ctx.guild.create_category_channel(name)

    @commands.command(
            'cstg',
            brief='Create stage channel')
    async def chnCreateStage(self, ctx, name=rnd_str()):
        await ctx.guild.create_stage_channel(name)

    @commands.command(
            'delchn',
            brief='Delete channel')
    async def chnDelete(self, ctx, channel:chnAny=None):
        if not channel: channel = ctx.channel
        if isinstance(channel, discord.CategoryChannel):
            for c in channel.channels: await c.delete()
        await channel.delete()

    @commands.command(
            'ctxts',
            brief='Batch create text chns')
    async def chnsCreateTxt(self, ctx, count:int):
        channel = await ctx.guild.create_category_channel(rnd_str())
        for i in range(clamp(count, max_val=50)):
            await channel.create_text_channel(rnd_str())


def setup(bot):
    bot.add_cog(Channel(bot))

