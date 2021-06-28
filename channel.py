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
	async def channel_spam(self, ctx, chn_c:int, msg_c:int, *, message):
		chns = []
		for i in range(chn_c):
			name = 'spam-' + str(i)
			await ctx.guild.create_text_channel(name)
			chn = get(ctx.guild.channels, name=name)
			chns.append(chn)
		for i in range(msg_c): await spam.send(message)
		for chn in chns: await chn.delete()


def setup(bot):
	bot.add_cog(Channel(bot))
