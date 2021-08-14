import discord
from discord.ext import commands

from dscord.func import clamp, rnd_str


class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        'spamsend',
        brief='Spam messages')
    async def spamSend(self, ctx, times: int, *, msg):
        for i in range(clamp(times)): await ctx.send(msg)

    @commands.command(
        'spamdir',
        brief='Spam dm member')
    async def spamDirect(self, ctx, user: discord.User, times: int, *, msg):
        for i in range(clamp(times)): await user.send(msg)

    @commands.command(
        'spamcs',
        brief='Spam channels & messages')
    async def chnMsgSpam(self, ctx, chn_num: int, msg_num: int, *, msg):
        cat = await ctx.guild.create_category_channel(rnd_str())
        for i in range(clamp(chn_num)): await cat.create_text_channel(rnd_str())
        for chn in cat.channels: [await chn.send(msg) for i in range(clamp(msg_num))]


def setup(bot):
    bot.add_cog(Spam(bot))
