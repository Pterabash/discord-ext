from discord.utils import get
from discord.ext import commands


class Channel(commands.Cog):
    def __init__(self, bot): self.bot = bot
        
    @commands.command('create')
    async def channel_create(self, ctx):
        await ctx.guild.create_text_channel('channel')

    @commands.command('delete')
    async def channel_delete(self, ctx):
        await ctx.channel.delete()

    @commands.command('cspam')
    async def channel_spam(self, ctx, chn_c:int, msg_c:int, *, message):
        chns = []
        for i in range(chn_c):
            name = 'spam-' + str(i)
            await ctx.guild.create_text_channel(name)
            chn = get(ctx.guild.channels, name=name)
            chns.append(chn)
            for i in range(msg_c): await spam.send(message)
	    for chn in chns: await chn.delete()


def setup(bot): bot.add_cog(Channel(bot))
