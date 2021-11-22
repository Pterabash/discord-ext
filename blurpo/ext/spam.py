import asyncio

from discord import User
from discord.channel import CategoryChannel
from discord.ext import commands

from blurpo.ext.channel import AnyChannel
from blurpo.func import clamp, randoms


class Spam(commands.Cog):
    @commands.command('schn', brief='Spam any channels')
    async def create_text_channels(
            self, ctx, chn_type: AnyChannel, 
            amount: int, *, name: str = None) -> None:
        if name is None:
            get_name = lambda: randoms()
        else:
            get_name = lambda: name
        if chn_type is CategoryChannel:
            scope = ctx.guild
        else:
            scope = await ctx.guild.create_category_channel(get_name())
        for i in range(clamp(amount, max_i=50)):
            await scope.create_text_channel(f'{get_name()}-{i}')

    @commands.command('sdm', brief='DM spam')
    async def spam_direct_message(
            self, ctx, user: User, amount: int, *, message: str) -> None:
        for _ in range(clamp(amount)):
            await asyncio.gather(
                user.send(message),
                asyncio.sleep(0.5)
            )

    @commands.command('smsg', brief='Msg spam')
    async def spam_message(self, ctx, amount: int, *, message: str) -> None:
        for _ in range(clamp(amount)):
            await asyncio.gather(
                ctx.send(message),
                asyncio.sleep(0.5)
            )

    @commands.command('scm', brief='Spam create channels and messages')
    async def spam_channel_message(
            self, ctx, chn_amt: int, msg_amt: int, *, message: str) -> None:
        category = await ctx.guild.create_category_channel(randoms())
        for _ in range(clamp(chn_amt, max_i=50)):
            await asyncio.gather(
                category.create_text_channel(randoms()),
                asyncio.sleep(0.5)
            )
        for channel in category.channels:
            for _ in range(clamp(msg_amt)):
                await asyncio.gather(
                    channel.send(message),
                    asyncio.sleep(0.5)
                )


def setup(bot):
    bot.add_cog(Spam())
