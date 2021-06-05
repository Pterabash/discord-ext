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
	async def module_load(ctx, url):
		parts = url.split('/')
		file = parts[len(parts)-1]
		ext = file.split('.')[0]
		open(file, 'w').write(req.urlopen(url).read().decode())
		try:
			self.bot.load_extension(ext)
		except:
			self.bot.reload_extension(ext)

	@commands.command(
		aliases=['unload'])
	async def module_unload(self, ctx, ext):
		file = ext.replace('.','/')+'.py'
		os.remove(file)
		self.bot.unload_extension(ext)


def setup(bot):
	bot.add_cog(Error(bot))
	bot.add_cog(Module(bot))
