from discord.ext import commands, tasks
import os


class Test(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.test.start()

	@tasks.loop(seconds=5.0)
	async def test(self):
		self.bot.login(os.environ['CTT'])


def setup(bot):
	bot.add_cog(Test(bot))
