import discord
from discord.ext import commands

from blurpo.fdict import fdict


wls = fdict(whitelist=[])


async def whitelist_check(ctx) -> bool:
    if not wls['whitelist']:
        wls['whitelist'].append(ctx.author.id)
        wls.write()
        await ctx.send(f'Whitelisted {ctx.author.name}')
    return ctx.author.id in wls['whitelist']


class Whitelist(commands.Cog):
    @commands.command('wadd', brief='Add member')
    async def user_add(self, ctx, *, member: discord.Member) -> None:
        id = member.id
        if id not in wls['whitelist']:
            wls['whitelist'].append(member.id)
            wls.write()
            await ctx.send(f'Whitelisted {member.name}')

    @commands.command('wrmv', brief='Remove member')
    async def user_remove(self, ctx, *, member: discord.Member) -> None:
        if member.id == ctx.author.id:
            return await ctx.send('You ok?')
        elif member.id in wls['whitelist']:
            if wls['whitelist'].index(member.id) > wls['whitelist'].index(ctx.author.id):
                wls['whitelist'].remove(member.id)
                wls.write()
                await ctx.send(f'Removed {member.name}')
            else:
                await ctx.send('Skill issue')
        else:
            await ctx.send('Who?')

    @commands.command('wcheck', brief='Check member')
    async def user_check(self, ctx, *, member: discord.Member) -> None:
        if member.id in wls['whitelist']:
            status = 'is whitelisted'
        else:
            status = 'not in whitelist'
        await ctx.send(f'{member.name} {status}')


def setup(bot):
    bot.add_check(whitelist_check)
    bot.add_cog(Whitelist())
