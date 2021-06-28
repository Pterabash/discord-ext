import random
import typing
import discord
from discord.utils import get
from discord.ext import commands


class Channel(commands.Cog):
	def __init__(self, bot): self.bot = bot

	@commands.command(
		'chntxt',
		brief='Create text channel')
	async def chnCreateText(self, ctx, name:str=None):
		if not name: name = 'general'
		await ctx.guild.create_text_channel(name)

	@commands.command(
		'chnvo',
		brief='Create voice channel')
	async def chnCreateVoice(self, ctx, name:str=None):
		if not name: name = 'General'
		await ctx.guild.create_voice_channel(name)

	@commands.command(
		'chncat',
		brief='Create category "channel"')
	async def chnCreateCategory(self, ctx, name:str=None):
		if not name: name = 'General'
		await ctx.guild.create_category_channel(name)

	@commands.command(
		'chnstg',
		brief='Create stage channel')
	async def chnCreateStage(self, ctx, name:str=None):
		if not name: name = 'General'
		await ctx.guild.create_stage_channel(name)

	@commands.command(
		'chndel',
		brief='Delete channel(s)')
	async def chnDelete(self, ctx, 
		channel:typing.Union[
			discord.StageChannel, 
			discord.CategoryChannel,
			discord.VoiceChannel,
			discord.TextChannel]=None):
		if not channel: await ctx.channel.delete()
		else:
			if isinstance(channel, discord.CategoryChannel):
				for c in channel.channels: await c.delete()
			await channel.delete()

	@commands.command(
		'chnspam',
		brief='Spam create channel and spam messages')
	async def chnSpam(self, ctx, chn_num:int, times:int, *, message):
		name = str(random.random())[2:]
		await ctx.guild.create_category_channel(name)
		category = get(ctx.guild.channels, name=name)
		for i in range(chn_num): await category.create_text_channel(name)
		for channel in ctx.guild.channels:
			if category == channel.category:
				for j in range(times): await channel.send(message)


def setup(bot):
	bot.add_cog(Channel(bot))
