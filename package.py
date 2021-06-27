import sys
import subprocess
from discord.ext import commands

class Package(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'pkginst',
		brief='Install Python package')
	async def pkgInstall(self, ctx, package: str):
		pass

def setup(bot):
	bot.add_cog(Package(bot))
