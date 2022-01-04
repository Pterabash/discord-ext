import os

import discord
from discord.ext import commands

from blurpo.func import EvalFile


wl = EvalFile('whitelist', val=[])


async def whitelist_check(ctx) -> bool:
    users = wl.get()
    if not users: 
        users = wl.append(ctx.author.id)
    return ctx.author.id in users


class Whitelist(commands.Cog):
    @commands.command('wadd', brief='Add member')
    async def user_add(self, ctx, *member: discord.Member) -> None:
        wl.add(member.id)
        await ctx.send(f'Whitelisted {member.name}')

    @commands.command('wrmv', brief='Remove member')
    async def user_remove(self, ctx, *member: discord.Member) -> None:
        if ctx.author.id == member.id:
            await ctx.send('Self removal is prohibited')
            return
        if member.id in wl.get():
            if wl.index(ctx.author.id) < wl.index(member.id):
                wl.remove(member.id)
                await ctx.send(f'Removed {member.name}')
            else:
                await ctx.send('Skill issue')
        else:
            await ctx.send('Member not whitelisted')

    @commands.command('wcheck', brief='Check member')
    async def user_check(self, ctx, *member: discord.Member) -> None:
        if member.id in wl.get():
            status = 'is whitelisted'
        else: 
            status = 'not in whitelist'
        await ctx.send(f'{member.name} {status}')


def setup(bot):
    bot.add_check(whitelist_check)
    bot.add_cog(Whitelist())
