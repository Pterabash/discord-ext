from discord.ext import commands
import os


class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def test(self, ctx):
		await self.bot.login(os.environ['CTT'])


def setup(bot):
	bot.add_cog(Test(bot))
