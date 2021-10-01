import discord
from discord.ext import commands

from dscord.func import Db, code_wrap

db = Db('whitelist')


async def check(ctx):
    if not db.vals():
        db.write(ctx.author.id)
        await ctx.send("You are whitelisted")
    return ctx.author.id in db.vals()


class Whitelist(commands.Cog):
    @commands.command('wadd', brief='Add member')
    async def add(self, ctx, member: discord.Member) -> None:
        db.write(member.id)
        await ctx.send("Welcome!")

    @commands.command('wcheck', brief='Check member')
    async def isAdded(self, ctx, member: discord.Member = None) -> None:
        if member:
            await ctx.send(f"{member.name} {'is whitelisted' if member.id in db.vals() else 'not in whitelist'}")
        else:
            await ctx.send(f'{len(db.keys())} user(s) whitelisted')
        
    @commands.command('wrmv', brief='Remove member')
    async def remove(self, ctx, member: discord.Member) -> None:
        wl = db.vals()
        if ctx.author.id == member.id:
            await ctx.send('No')
        elif member.id in wl:
            if wl.index(ctx.author.id) < wl.index(member.id):
                db.erase(str(member.id))
                await ctx.send('Get banished')
            else:
                await ctx.send('Skill issue')
        else:
            await ctx.send('Member not in whitelist')



def setup(bot):
    bot.add_check(check)
    bot.add_cog(Whitelist())
