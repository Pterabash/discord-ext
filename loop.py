import discord, asyncio, os
from discord.ext import commands, tasks


class Fun(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.check = False

	@commands.command()
	async def burn(self, ctx):
		self.check = True
		while self.check:
			await ctx.send('<@450360653094584340>')
			await asyncio.sleep(30)

	@commands.command()
	async def stop(self, ctx):
		self.check = False

	@commands.Cog.listener()
	async def on_message(self, ctx):
		if ctx.author.id==394771663155101727:
			await ctx.send('jews')


def setup(bot):
	bot.add_cog(Fun(bot))
