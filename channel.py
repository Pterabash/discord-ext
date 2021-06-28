import random
import typing
import discord
from discord.utils import get
from discord.ext import commands

chnAny = typing.Union[
	discord.StageChannel,
	discord.CategoryChannel,
	discord.VoiceChannel,
	discord.TextChannel]

def intCheck(num):
	if num < 1: num = 1
	elif num > 100: num = 100
	return num


class Channel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'ccrtxt',
		brief='Create text channel')
	async def chnCreateText(self, ctx, name=None):
		if not name: name = 'text'
		await ctx.guild.create_text_channel(name)

	@commands.command(
		'ccrvo',
		brief='Create voice channel')
	async def chnCreateVoice(self, ctx, name=None):
		if not name: name = 'Voice'
		await ctx.guild.create_voice_channel(name)

	@commands.command(
		'ccrcat',
		brief='Create category "channel"')
	async def chnCreateCategory(self, ctx, name=None):
		if not name: name = 'Category'
		await ctx.guild.create_category_channel(name)

	@commands.command(
		'ccrstg',
		brief='Create stage channel')
	async def chnCreateStage(self, ctx, name=None):
		if not name: name = 'Stage'
		await ctx.guild.create_stage_channel(name)

	@commands.command(
		'chndel',
		brief='Delete channel(s)')
	async def chnDelete(self, ctx, channel:chnAny=None):
		if not channel: await ctx.channel.delete()
		else:
			if isinstance(channel, discord.CategoryChannel):
				for c in channel.channels: await c.delete()
			await channel.delete()

	@commands.command(
		'chninfo',
		brief='Get channel information')
	async def chnInfo(self, ctx, channel:chnAny=None):
		if not channel: channel = ctx.channel
		attr = ['category', 'created_at', 'guild', 'name', 'permissions_synced', 'position']
		l = []
		for a in attr:
			value = getattr(channel, a)
			l.append(a+': '+str(value))
		msg = '```\n' + '\n'.join(l) + '```'
		await ctx.send(msg)

	@commands.command(
		'spamcs',
		brief='Spam create channels & send messages')
	async def chnCreateSpamMsg(self, ctx, chn_num:int, times:int, *, message):
		chn_num, times = intCheck(chn_num), intCheck(times)
		cat = random.random()
		await ctx.guild.create_category_channel(cat)
		category = get(ctx.guild.channels, name=cat)
		for i in range(chn_num): await category.create_text_channel(random.random())
		for channel in category.channels:
		for j in range(times): await channel.send(message)
		await channel.delete()


def setup(bot):
	bot.add_cog(Channel(bot))
