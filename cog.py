import os
import urllib.request as req
from discord.ext import commands


class Error(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		if isinstance(err, commands.CommandNotFound): 
			return
		await ctx.send(err)


class Module(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		aliases=['load'])
	async def module_load(self, ctx, url):
		ext = ext_setup(url)
		self.bot.load_extension(ext)

	@commands.command(
		aliases=['reload'])
	async def module_reload(self, ctx, url):
		ext = ext_setup(url)
		self.bot.reload_extension(ext)

	@commands.command(
		aliases=['unload'])
	async def module_unload(self, ctx, ext):
		os.remove(ext.replace('.','/')+'.py')
		self.bot.unload_extension(ext)


def ext_setup(url):
	x = url.split('/')
	y = x[len(x)-1]
	open(y,'w').write(req.urlopen(url).read().decode())
	return y.replace('.py','').replace('/','.')

def setup(bot):
	bot.add_cog(Error(bot))
	bot.add_cog(Module(bot))
