from discord import User
from discord.ext import commands

from dscord.func import clamp


class Message(commands.Cog):
    @commands.command('dm', brief='Dm user')
    async def direct(self, ctx, user: User = None, *, message: str):
        if not user: user = ctx.author
        await user.send(message)

    @commands.command('msgdel', brief='Delete msgs')
    async def delete(self, ctx, num: int = 1):
        num = clamp(num + 1)
        logs = []
        async for log in ctx.channel.history(limit=num): logs.append(log)
        await ctx.channel.delete_messages(logs)

    @commands.command('msgsend', aliases=['say','echo'], brief='Send msg')
    async def send(self, ctx, *, message: str):
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Message())
