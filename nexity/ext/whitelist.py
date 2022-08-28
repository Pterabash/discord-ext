import discord
from discord.ext import commands

from nexity.util import load_data, save_data


data = load_data({'whitelist': []})


async def whitelist_check(ctx) -> bool:
    if not data['whitelist']:
        data['whitelist'].append(ctx.author.id)
        save_data(data)
        await ctx.send(f'Whitelisted {ctx.author.name}')
    return ctx.author.id in data['whitelist']


class Whitelist(commands.Cog):
    @commands.command('wadd', brief='Add member')
    async def user_add(self, ctx, *, member: discord.Member) -> None:
        id = member.id
        if id not in data['whitelist']:
            data['whitelist'].append(member.id)
            save_data(data)
            await ctx.send(f'Whitelisted {member.name}')

    @commands.command('wrmv', brief='Remove member')
    async def user_remove(self, ctx, *, member: discord.Member) -> None:
        if member.id == ctx.author.id:
            return await ctx.send('You ok?')
        elif member.id in data['whitelist']:
            if data['whitelist'].index(member.id) > data['whitelist'].index(ctx.author.id):
                data['whitelist'].remove(member.id)
                save_data(data)
                await ctx.send(f'Removed {member.name}')
            else:
                await ctx.send('Skill issue')
        else:
            await ctx.send('Who?')

    @commands.command('wcheck', brief='Check member')
    async def user_check(self, ctx, *, member: discord.Member) -> None:
        if member.id in data['whitelist']:
            status = 'is whitelisted'
        else:
            status = 'not in whitelist'
        await ctx.send(f'{member.name} {status}')


def setup(bot):
    bot.add_check(whitelist_check)
    bot.add_cog(Whitelist())
