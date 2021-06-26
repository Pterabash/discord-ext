from discord.ext import commands

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound): return
        print(error)
        if isinstance(err, commands.CheckFailure): return
        await ctx.send(err)

def setup(bot): bot.add_cog(Error(bot))
