from discord.ext import commands, tasks
import os


class Task(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.test.start()

	@tasks.loop(seconds=5.0)
	async def test(self):
		self.bot.login(os.environ['ctt'])


def setup(bot):
	bot.add_cog(Task(bot))
