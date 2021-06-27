import discord
from discord.ext import commands

def numCheck(num):
	if num < 1: num = 1
	elif num > 100: num = 100
	return num

class Message(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
        
	@commands.command(
		'msgdel',
		brief='Delete messages')
	async def msgDelete(self, ctx, num: int):
		num = numCheck(num) + 1
		logs = []
		async for log in ctx.channel.history(limit=num): logs.append(log)
		await ctx.channel.delete_messages(logs)

	@commands.command(
		'msgsend',
		aliases=['say', 'echo', 'print'],
		brief='Send message')
	async def msgSend(self, ctx, *, message):
		await ctx.send(message)

	@commands.command(
		'msgspam',
		aliases=['repeat', 'spam'],
		brief='Spam messages')
	async def msgSpam(self, ctx, times: int, *, message):
		times = numCheck(times)
		for i in range(times): await ctx.send(message)

	@commands.command(
		'msgdir',
		aliases=['dm'],
		brief='Dm member')
	async def msgDirect(self, ctx, member:discord.Member, *, message):
		await member.send(message)

	@commands.command(
		'msgdirspam'
		aliases=['dmspam']
		brief='Spam dm member')
	async def direct_spam(self, ctx, times: int, member:discord.Member, *, message):
		times = numCheck(times)
		for i in range(times): await member.send(message)


def setup(bot):
	bot.add_cog(Message(bot))
