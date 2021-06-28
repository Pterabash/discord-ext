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
		brief='Delete a channel')
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
	async def chnSpam(self, ctx, chn_num:int=10, times:int=4, *, message):
		cat = str(random.random())
		await ctx.guild.create_category_channel(cat)
		catChn = get(ctx.guild.channels, name=cat)
		for i in range(chn_num):
			txt = str(random.random())
			await catChn.create_text_channel(txt)
			txtChn = get(catChn, name=txt)
			for j in range(times): await txtChn.send(message)
		for c in catChn: await c.delete()
		await catChn.delete()


def setup(bot):
	bot.add_cog(Channel(bot))
