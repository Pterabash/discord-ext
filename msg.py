import discord
from discord.ext import commands


class Message(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	# ctx based messaging
	@commands.command('clear')
	async def message_clear(self, ctx, num: int):
		num += 1
		if num <= 1: num = 2
		elif num > 100: num = 100
		logs = []
		async for log in ctx.channel.history(limit=num):
			logs.append(log)
		await ctx.channel.delete_messages(logs)

	@commands.command('say')
	async def message_say(self, ctx, *, message):
		await ctx.send(message)

	@commands.command('spam')
	async def message_spam(self, ctx, count:int, *, message):
		for i in range(count):
			await ctx.send(message)

	# user based messaging
	@commands.command('dm')
	async def direct_message(self, ctx, member:discord.Member=None, *, message):
		await member.send(message)

	@commands.command('dspam')
	async def direct_spam(self, ctx, count:int, member:discord.Member, *, message):
		for i in range(count):
			await member.send(message)


def setup(bot):
	bot.add_cog(Message(bot))
