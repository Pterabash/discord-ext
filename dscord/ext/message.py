import discord
from discord.ext import commands


class Message(commands.Cog):
    @commands.command(
        'send', brief='Send message', aliases=['say', 'echo']
    )
    async def send_message(self, ctx, *, message: str) -> None:
        await ctx.send(message)
    
    @commands.command('direct', brief='DM user', aliases=['dm'])
    async def direct_message(
        self, ctx, user: discord.User = None, *, message: str
    ) -> None:
        await user.send(message)

    @commands.command('mdel', brief='Delete messages by ID')
    async def delete_messages(self, ctx, *ids: discord.Message):
        for i in ids:
            try:
                await i.delete()
            except Exception as e:
                print(e)

    @commands.command('purge', brief='Purge messages')
    async def purge_messages(self, ctx, amount: int = 1) -> None:
        await ctx.channel.purge(limit=amount)

    @commands.command('purgemember', brief='Purge member messages')
    async def purge_member_messages(
        self, ctx, member: discord.Member, amount: int = 1
    ) -> None:
        msgs = []
        for m in ctx.channel.history():
            if len(msgs) == amount:
                break
            if m.author == member:
                msgs.append(m)
        await ctx.channel.delete_messages(msgs)


def setup(bot):
    bot.add_cog(Message())
