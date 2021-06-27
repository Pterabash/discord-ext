import sys
import tempfile
import subprocess
from discord.ext import commands

def pipRun(action, package, inp=None):
	with tempfile.TemporaryFile('r+t') as tp:
		subprocess.run(
			args=[sys.executable, '-m', 'pip', action, package],
                        input=inp,
			stdout=tp,
			stderr=subprocess.STDOUT)
		tp.seek(0)
		return tp.read()


class Package(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'pkginst',
		aliases=['pkgadd'],
		brief='Install Python package')
	async def pkgInstall(self, ctx, package: str):
		await ctx.send(pipRun('install', package))

	@commands.command(
		'pkgunst',
		aliases=['pkgrmv'],
		brief='Uninstall Python package')
	async def pkgUninstall(self, ctx, package: str):
		await ctx.send(pipRun('uninstall', package, 'y'))


def setup(bot):
	bot.add_cog(Package(bot))
