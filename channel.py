import random
import typing
import discord
from discord.utils import get
from discord.ext import commands

def intCheck(num):
	if num < 1: num = 1
	elif num > 100: num = 100
	return num

async def chnsCreate(chn_num):
	cat = random.random()
	await ctx.guild.create_category_channel(cat)
	category = get(ctx.guild.channels, name=cat)
	for i in range(chn_num): await category.create_text_channel(random.random())


class Channel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'crtxt',
		brief='Create text channel')
	async def chnCreateText(self, ctx, name=None):
		if not name: name = 'general'
		await ctx.guild.create_text_channel(name)

	@commands.command(
		'crvo',
		brief='Create voice channel')
	async def chnCreateVoice(self, ctx, name=None):
		if not name: name = 'General'
		await ctx.guild.create_voice_channel(name)

	@commands.command(
		'crcat',
		brief='Create category "channel"')
	async def chnCreateCategory(self, ctx, name=None):
		if not name: name = 'General'
		await ctx.guild.create_category_channel(name)

	@commands.command(
		'crstg',
		brief='Create stage channel')
	async def chnCreateStage(self, ctx, name=None):
		if not name: name = 'General'
		await ctx.guild.create_stage_channel(name)

	@commands.command(
		'chndel',
		brief='Delete channel(s)')
	async def chnDelete(self, ctx, channel:typing.Union[discord.StageChannel, discord.CategoryChannel, discord.VoiceChannel, discord.TextChannel]=None):
		if not channel: await ctx.channel.delete()
		else:
			if isinstance(channel, discord.CategoryChannel):
				for c in channel.channels: await c.delete()
			await channel.delete()

	@commands.command(
		'spamchn',
		brief='Spam create channels')
	async def chnCreateSpam(self, ctx, chn_num: int):
		chn_num = intCheck(chn_num)
		chnsCreate(chn_num)

	@commands.command(
		'spamcm',
		brief='Spam create channels & send messages')
	async def chnCreateSpamMsg(self, ctx, chn_num:int, times:int, *, message):
		chn_num, times = intCheck(chn_num), intCheck(times)
		chnsCreate(chn_num)
		for channel in category.channels:
			for j in range(times): await channel.send(message)
			await channel.delete()


def setup(bot):
	bot.add_cog(Channel(bot))
