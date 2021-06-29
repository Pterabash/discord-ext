import discord
from discord.ext import commands

class User(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def botMorph(self, ctx, member:discord.Member=None):
		if not member: await self.bot.user.edit(username='Bot User', avatar=None)
		else:
			await self.bot.user.edit(
				username=member.name,
				avatar=member.avatar_url.read())

def setup(bot):
	bot.add_cog(User(bot))

