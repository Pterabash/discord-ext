import sys
import subprocess
from discord.ext import commands

def pipInstall(package): 
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package]) 

def pipUninstall(package): 
    subprocess.check_call([sys.executable, '-m', 'pip', 'uninstall', package])


class Package(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'pkginst',
		aliases=['pkgrmv'],
		brief='Install Python package')
	async def pkgInstall(self, ctx, package: str):
		pipInstall(package)

	@commands.command(
		'pkgunst',
		aliases=['pkgrmv'],
		brief='Uninstall Python package')
	async def pkgUninstall(self, ctx, package: str):
		pipUninstall(package)


def setup(bot):
	bot.add_cog(Package(bot))
