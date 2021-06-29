import shelve
import tempfile
import subprocess
from discord.ext import commands

def bashList():
	with shelve.open('bash', 'c') as sh:
		return [sh[key] for key in sh.keys()]

def bashAdd(name, cmds):
	with shelve.open('bash', 'c') as sh:
		sh[name] = cmds

def bashRmv(name):
	with shelve.open('bash', 'c') as sh:
		del sh[name]

def bashRun(name):
	with shelve.open('bash', 'c') as sh:
		with tempfile.TemporaryFile('r+t') as tp:
			subprocess.run(args=sh[name], stdout=tp, stderr=subprocess.STDOUT, timeout=10)
			tp.seek(0)
			log = tp.read()
			x = 2000
			return [log[y-x:y] for y in range(x,len(log)+x,x)]


class Program(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'bashlist',
		brief='List bash command snippets')
	async def prgmBashList(self, ctx):
		await ctx.send('```\n'+'\n'.join(bashList())+'```')

	@commands.command(
		'bashadd',
		brief='Add bash commands snippet')
	async def prgmBashAdd(self, ctx, name, *cmds):
		bashAdd(name, cmds)

	@commands.command(
		'bashrmv',
		brief='Remove bash commands snippet')
	async def prgmBashRemove(self, ctx, name):
		cmdRmv(name)

	@commands.command(
		'bashrun',
		brief='Run bash commands snippet')
	async def prgmBashRun(self, ctx, name):
		cmdAdd(name)


def setup(bot):
	bot.add_cog(Program(bot))
