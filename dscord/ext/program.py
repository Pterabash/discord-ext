from tempfile import NamedTemporaryFile as ntf

from discord.ext import commands

from dscord.func import log_proc


class Program(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('sh')
    async def prgmBash(self, ctx, *cmds):
        for x in log_proc(cmds): await ctx.send(x)

    @commands.command('py')
    async def prgmPython(self, ctx, *, code):
        with ntf('r+t', suffix='.py') as tp:
            tp.write(code)
            tp.seek(0)
            for x in log_proc(['python', tp.name]): await ctx.send(x)

    @commands.command('js')
    async def prgmJavascript(self, ctx, *, code):
        with ntf('r+t', suffix='.js') as tp:
            tp.write(code)
            tp.seek(0)
            for x in log_proc(['node', tp.name]): await ctx.send(x)

    @commands.command('java')
    async def prgmJava(self, ctx, *, code):
        with ntf('r+t', suffix='.java') as tp:
            tp.write(code)
            tp.seek(0)
            for x in log_proc(['java', tp.name]): await ctx.send(x)

    @commands.command('r')
    async def prgmR(self, ctx, *, code):
        with ntf('r+t', suffix='.r') as tp:
            tp.write(code)
            tp.seek(0)
            for x in log_proc(['Rscript', tp.name]): await ctx.send(x)


def setup(bot):
    bot.add_cog(Program(bot))
