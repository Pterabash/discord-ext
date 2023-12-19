import asyncio
import discord
from discord.ext import commands

from nexity.util import load_data, save_data


data = load_data(whitelist=[])
wls = data['whitelist']


async def whitelist_check(ctx) -> bool:
    if not wls:
        wls.append(ctx.author.id)
        save_data(data)
        await ctx.send(f'Whitelisted {ctx.author.name}')
    return ctx.author.id in wls


class Whitelist(commands.Cog):
    @commands.command('wadd', brief='Add member')
    async def user_add(self, ctx, *, member: discord.Member) -> None:
        id = member.id
        if id not in wls:
            wls.append(member.id)
            save_data(data, whitelist=wls)
            await ctx.send(f'Whitelisted {member.name}')

    @commands.command('wrmv', brief='Remove member')
    async def user_remove(self, ctx, *, member: discord.Member) -> None:
        if member.id == ctx.author.id:
            return await ctx.send('You ok?')
        elif member.id in wls:
            if wls.index(member.id) > wls.index(ctx.author.id):
                wls.remove(member.id)
                save_data(data, whitelist=wls)
                await ctx.send(f'Removed {member.name}')
            else:
                await ctx.send('Skill issue')
        else:
            await ctx.send('Who?')

    @commands.command('wcheck', brief='Check member')
    async def user_check(self, ctx, *, member: discord.Member) -> None:
        status = 'is whitelisted' if member.id in wls else 'not in whitelist'
        await ctx.send(f'{member.name} {status}')


def setup(bot):
    bot.add_check(whitelist_check)
    async def cog(): 
        await bot.add_cog(Whitelist())
    asyncio.run(cog)
