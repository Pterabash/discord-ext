from discord import User
from discord.ext import commands

from dscord.func import clamp


class Message(commands.Cog):
    @commands.command('mdir', brief='DM user', aliases=['dm'])
    async def direct(self, ctx, user: User = None, *, message: str) -> None:
        if not user: user = ctx.author
        await user.send(message)

    @commands.command('mdel', brief='Delete msgs')
    async def delete(self, ctx, num: int = 1) -> None:
        num = clamp(num + 1)
        logs = []
        async for log in ctx.channel.history(limit=num): logs.append(log)
        await ctx.channel.delete_messages(logs)

    @commands.command('msend', brief='Send msg', aliases=['say','echo'])
    async def send(self, ctx, *, message: str) -> None:
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Message())
