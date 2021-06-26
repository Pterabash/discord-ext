import shelve
import discord
from discord.ext import commands

def idAdd(id):
	with shelve.open('whitelists', 'c') as wls:
		wls[str(id)] = id

def idRmv(id):
	with shelve.open('whitelists', 'c') as wls:
		del wls[str(id)]

def idRead():
	with shelve.open('whitelists', 'c') as wls:
		return [wls[key] for key in wls.keys()]

async def wlCheck(ctx):
	if not wls.keys(): idAdd(ctx.author.id)
	await ctx.send(ctx.author.id in idRead())
	return True #ctx.author.id in idRead()


class Whitelist(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command('wl', brief='Get whitelist')
	async def wlGet(self, ctx):
		for id in idRead(): await ctx.send(id)

	@commands.command('add', brief='Add member to whitelist')
	async def wlAdd(self, ctx, member:discord.Member):
		idAdd(member.id)

	@commands.command('rmv', brief='Remove member from whitelist')
	async def wl_rmv(self, ctx, member:discord.Member):
		if ctx.author.id != member.id:
			idRmv(member.id)
		else: await ctx.send('Why remove yourself?')


def setup(bot):
	bot.add_check(wlCheck)
	bot.add_cog(Whitelist(bot))
