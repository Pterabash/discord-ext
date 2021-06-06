from discord.ext import commands
from urllib.request import urlopen
import os


class test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


class Login(test):
	@commands.command()
	async def login(self, ctx):
		await self.bot.login(os.environ['CTT'])


def setup(bot):
	bot.add_cog(Login(bot))
