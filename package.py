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
		log = tp.read()
		x = 2000
		return [log[y-x:y] for y in range(x,len(stdout)+x,x)]


class Package(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'pkginst',
		aliases=['pkgadd'],
		brief='Install Python package')
	async def pkgInstall(self, ctx, package: str):
		for chunk in pipRun('install', package): await ctx.send(chunk)
		

	@commands.command(
		'pkgunst',
		aliases=['pkgrmv'],
		brief='Uninstall Python package')
	async def pkgUninstall(self, ctx, package: str):
		for chunk in pipRun('uninstall', package, b'y'): await ctx.send(chunk)


def setup(bot):
	bot.add_cog(Package(bot))
