import tempfile
import subprocess
from discord.ext import commands

def prgmRun(args):
	with tempfile.TemporaryFile('r+t') as tp:
		subprocess.run(
			args=args,
			stdout=tp,
			stderr=subprocess.STDOUT,
			timeout=10)
		tp.seek(0)
		log = tp.read()
		x = 2000
		return [log[y-x:y] for y in range(x,len(log)+x,x)]


class Program(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		'bashrun',
		brief='Run subprocess')
	async def prgmBashRun(self, ctx, *cmds):
		for chunk in prgmRun(cmds): await ctx.send(chunk)


def setup(bot):
	bot.add_cog(Program(bot))
