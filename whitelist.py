import discord
from discord.ext import commands

def whitelist(): return open('whitelist').read()


class Whitelist(commands.Cog):
    def __init__(self, bot): self.bot = bot

    @commands.command()
    async def add(self, ctx, member:discord.Member):
        member_name, member_id = member.name, str(member.id)
        if str(member.id) not in whitelist():
            open('whitelist', 'a').write('\n' + member_name + ' - ' + member_id)

    @commands.command()
    async def whitelist(self, ctx): await ctx.send(whitelist())


def setup(bot): bot.add_cog(Whitelist(bot))
