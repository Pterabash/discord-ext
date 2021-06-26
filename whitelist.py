import shelve
import discord
from discord.ext import commands

def idRead():
	with shelve.open('whitelists', 'c') as wls:
		return [wls[key] for key in wls.keys()]

def idAdd(id):
	with shelve.open('whitelists', 'c') as wls:
		wls[str(id)] = id

def idRmv(id):
	with shelve.open('whitelists', 'c') as wls:
		del wls[str(id)]

async def wlCheck(ctx):
	if not idRead(): idAdd(ctx.author.id)
	return ctx.author.id in idRead()


class Whitelist(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command('wlget', brief='Get whitelist')
	async def wlGet(self, ctx):
		for id in idRead(): await ctx.send(id)

	@commands.command('wladd', brief='Add member to whitelist')
	async def wlAdd(self, ctx, member:discord.Member):
		idAdd(member.id)

	@commands.command('wlrmv', brief='Remove member from whitelist')
	async def wlRmv(self, ctx, member:discord.Member):
		if ctx.author.id != member.id: idRmv(member.id)
		else: await ctx.send('Why remove yourself?')


def setup(bot):
	bot.add_check(wlCheck)
	bot.add_cog(Whitelist(bot))
