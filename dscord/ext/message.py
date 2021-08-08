import discord
from discord.ext import commands

from dscord.func import clamp


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
            'msgsend',
            brief='Send message')
    async def msgSend(self, ctx, *, message):
        await ctx.send(message)

    @commands.command(
            'msgdir',
            aliases=['dm'],
            brief='Dm member')
    async def msgDirect(self, ctx, user: discord.User, *, message):
        await user.send(message)

    @commands.command(
            'msgdel',
            brief='Delete messages')
    async def msgDelete(self, ctx, num: int):
        num = clamp(num + 1)
        logs = []
        async for log in ctx.channel.history(limit=num): logs.append(log)
        await ctx.channel.delete_messages(logs)


def setup(bot):
    bot.add_cog(Message(bot))

