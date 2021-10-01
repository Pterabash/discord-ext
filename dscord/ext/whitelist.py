import shelve

import discord
from discord.ext import commands


database = lambda : shelve.open('Database')


async def check(ctx) -> bool:
    with database() as db:
        if 'Whitelist' in db: 
            return ctx.author.id in db['Whitelist']
        else:
            db['Whitelist'] = [ctx.author.id]
            await ctx.send('You are whitelisted')
            return True


class Whitelist(commands.Cog):
    @commands.command('wadd', brief='Add member')
    async def add(self, ctx, member: discord.Member) -> None:
        with database() as db:
            db['Whitelist'].append(member.id)
            print(db) # Debug
        await ctx.send(f'Whitelisted {member.name}')

    @commands.command('wrmv', brief='Remove member')
    async def remove(self, ctx, member: discord.Member) -> None:
        if ctx.author.id == member.id:
            await ctx.send('Self removing is prohibited')
            return
        with database() as db:
            wl = db['Whitelist']
            if member.id in wl:
                if wl.index(ctx.author.id) < wl.index(member.id):
                    wl.remove(member.id)
                    await ctx.send(f'Removed {member.name}')
                else:
                    await ctx.send('Skill issue')
            else:
                await ctx.send('Member not whitelisted')

    @commands.command('wcheck', brief='Check member')
    async def isAdded(self, ctx, member: discord.Member = None) -> None:
        with database() as db:
            status = 'is whitelisted' if member.id in db['Whitelist'] else 'not in whitelist'
            await ctx.send(f'{member.name} {status}')


def setup(bot):
    bot.add_check(check)
    bot.add_cog(Whitelist())
