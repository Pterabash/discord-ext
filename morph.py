import discord
from discord.ext import commands

class morph(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def morph(self, ctx, member:discord.Member=None):
        if member is None:
            member = ctx.message.author
        await member.avatar_url.save('pfp')
        await self.bot.user.edit(
                username=member.name,
                avatar=open('pfp','rb').read())

def setup(bot): bot.add_cog(morph(bot))

