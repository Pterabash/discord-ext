import discord
from discord.ext import commands

from dscord.func import Db, code_wrap

wl = Db('whitelist')


async def wlCheck(ctx):
    if not wl.readval(): wl.write(ctx.author.id)
    in_list = ctx.author.id in wl.readval()
    if not in_list: await ctx.send('`Your opinion has been rejected.`')
    return in_list


class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('wl', brief='Get whitelist')
    async def wlGet(self, ctx):
        for x in code_wrap('\n'.join(wl.readkey())): await ctx.send(x)

    @commands.command('wladd', brief='Add member to whitelist')
    async def wlAdd(self, ctx, member: discord.Member):
        wl.write(member.id)

    @commands.command('wlrmv', brief='Remove member from whitelist')
    async def wlRmv(self, ctx, member: discord.Member):
        if ctx.author.id != member.id:
            wl.erase(member.id)
        else:
            await ctx.send('Why remove yourself?')


def setup(bot):
    bot.add_check(wlCheck)
    bot.add_cog(Whitelist(bot))
