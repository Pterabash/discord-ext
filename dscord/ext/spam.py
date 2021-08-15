from discord import User
from discord.ext import commands

from dscord.func import clamp, rng_str


class Spam(commands.Cog):
    @commands.command('cmspam', brief='Chn & msg spam')
    async def channelMessage(self, ctx, channel_count: int, message_count: int, *, message: str):
        cc, mc = clamp(channel_count), clamp(message_count)
        category = await ctx.guild.create_category_channel(rng_str())
        for _ in range(cc):
            await category.create_text_channel(rng_str())
        for channel in category.channels:
            for _ in range(mc):
                await channel.send(message)

    @commands.command('dmspam', brief='DM spam')
    async def directMessage(self, ctx, user: User, count: int, *, message: str):
        c = clamp(count)
        for _ in range(c):
            await user.send(message)

    @commands.command('msgspam', brief='Msg spam')
    async def message(self, ctx, count: int, *, message: str):
        c = clamp(times)
        for _ in range(c):
            await ctx.send(message)


def setup(bot):
    bot.add_cog(Spam())
