import discord
from descord.func import Db
from discord.ext import commands

wl = Db('whitelist.db')

async def wlCheck(ctx):
    if not wl.readval(): wl.write(ctx.author.id)
    return ctx.author.id in wl.readval()


class Whitelist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('wl', brief='Get whitelist')
    async def wlGet(self, ctx):
        await ctx.send(code_wrap('\n'.join(wl.readkey())))

    @commands.command('wladd', brief='Add member to whitelist')
    async def wlAdd(self, ctx, member:discord.Member):
        wl.write(member.id)

    @commands.command('wlrmv', brief='Remove member from whitelist')
    async def wlRmv(self, ctx, member:discord.Member):
        if ctx.author.id != member.id: wl.erase(member.id)
        else: await ctx.send('Why remove yourself?')


def setup(bot):
    bot.add_check(wlCheck)
    bot.add_cog(Whitelist(bot))

