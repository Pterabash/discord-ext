import subprocess
from discord.ext import commands

def prog_open(file, code):
	open(file, 'w').write(code)

def prog_run(stdout, *args):
	subprocess.run(args=args,
		stdout=open(stdout, 'w'),
		stderr=subprocess.STDOUT,
		timeout=10)

def prog_out(file):
	stdout = open(file).read()
	x = 2000
	chunks = [stdout[y - x:y] for y in range(x, len(stdout) + x, x)]
	return chunks


class Programming(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		brief='popen(); prun(path); inp')
	async def addlang(self, ctx, ext, *, run):
		run = run.replace('\n', '\n	')
		code = f'''import subprocess
import prog
from discord.ext import commands

inp = 'inp'
outp = 'outp'

@commands.command()
async def {ext}(ctx, *, code):
	path = inp + '.{ext}'
	{run}
	for chunk in prog.prog_out(outp):
		await ctx.send(chunk)

def setup(bot):
	bot.add_command({ext})'''
		code = code.replace('popen()', 'prog.prog_open(path, code) ')
		code = code.replace('prun(', 'prog.prog_run(outp, ')
		open(ext + '.py', 'w').write(code)
		try:
			self.bot.unload_extension(ext)
		except:
			pass
		self.bot.load_extension(ext)


def setup(bot):
	bot.add_cog(Programming(bot))
