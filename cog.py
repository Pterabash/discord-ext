import os
from urllib.request import urlopen
from discord.ext import commands


class Main(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_command_error(self, ctx, err):
		if isinstance(err, commands.CommandNotFound): return
		await ctx.send(err)

	@commands.command()
	async def load(self, ctx, url):
		file = url.split('/')[-1]
		ext = file.split('.')[0]
		open(file, 'w').write(urlopen(url).read().decode())
		try: self.bot.reload_extension(ext)
		except: self.bot.load_extension(ext)

	@commands.command()
	async def unload(self, ctx, ext):
		file = ext.replace('.','/')+'.py'
		os.remove(file)
		self.bot.unload_extension(ext)


def setup(bot):
	bot.add_cog(Main(bot))

