import sys
import tempfile
import subprocess
from discord.ext import commands

async def pipRun(ctx, *args):
	with tempfile.TemporaryFile('r+t') as tp:
		subprocess.check_call(
			args=[sys.executable, '-m', 'pip']+args,
			stdout=tp,
			stderr=subprocess.STDOUT)
		tf.seek(0)
		await ctx.cend('```py\n'+tp.read()+'```')


class Package(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'pkginst',
		aliases=['pkgadd'],
		brief='Install Python package')
	async def pkgInstall(self, ctx, package: str):
		await pipRun(ctx, 'install', package)

	@commands.command(
		'pkgunst',
		aliases=['pkgrmv'],
		brief='Uninstall Python package')
	async def pkgUninstall(self, ctx, package: str):
		await pipRun(ctx, 'uninstall', package)


def setup(bot):
	bot.add_cog(Package(bot))
