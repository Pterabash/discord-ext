import discord
from discord.ext import commands

from nexity.util import clamp


class Message(commands.Cog):
    @commands.command(
            'send', brief='Send message', aliases=['say', 'echo'])
    async def send_message(self, ctx, *, message: str) -> None:
        await ctx.send(message)
    
    @commands.command('direct', brief='DM user', aliases=['dm'])
    async def direct_message(
            self, ctx, user: discord.User = None, *, message: str) -> None:
        await user.send(message)

    @commands.command('mdel', brief='Delete messages by ID')
    async def delete_messages(self, ctx, *ids: discord.Message):
        for i in ids:
            await i.delete()
        await ctx.delete()

    @commands.command('purge', brief='Purge messages')
    async def purge_messages(self, ctx, amount: int = 1) -> None:
        await ctx.channel.purge(limit=clamp(amount+1))

    @commands.command('purgemember', brief='Purge member messages')
    async def purge_member_messages(
        self, ctx, member: discord.Member, amount: int = 1) -> None:
        msgs = []
        async for m in ctx.channel.history():
            if len(msgs) == amount:
                break
            if m.author == member:
                msgs.append(m)
        await ctx.channel.delete_messages(msgs)


async def setup(bot):
    await bot.add_cog(Message())
