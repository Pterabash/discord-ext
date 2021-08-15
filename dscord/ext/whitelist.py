from discord import Member
from discord.ext import commands

from dscord.func import Db, code_wrap

db = Db('whitelist')


async def check(ctx):
    if not db.vals():
        db.write(ctx.author.id)
        await ctx.send("You are whitelisted")
    return ctx.author.id in db.vals()


class Whitelist(commands.Cog):
    @commands.command('wladd', brief='Add member')
    async def add(self, ctx, member: Member):
        db.write(member.id)
        await ctx.send("Welcome!")

    @commands.command('wlcheck', brief='Check member')
    async def isAdded(self, ctx, member: Member):
        if member.id in db.vals():
            await ctx.send("Member is whitelisted")
        else:
            await ctx.send("Member not in whitelist")
        
    @commands.command('wlrmv', brief='Remove member')
    async def remove(self, ctx, member: Member):
        if ctx.author.id == member.id: await ctx.send('No')
        else: 
            db.erase(str(member.id))
            await ctx.send("Get banished")


def setup(bot):
    bot.add_check(check)
    bot.add_cog(Whitelist())
