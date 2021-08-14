import os
from tempfile import NamedTemporaryFile
from typing import List

from discord.ext import commands

from dscord.func import log_proc


class Program(commands.Cog):
    class Execute:
        def __init__(self, suffix:str, command: List[str]) -> List[str]:
            self.suffix = f'.{suffix}'
            self.command = command

        def output(self, code: str):
            with NamedTemporaryFile('r+t', suffix=self.suffix) as tp:
                tp.write(code)
                tp.seek(0)
                os.system(f'chmod +x {tp.name}')
                return log_proc(self.command+[tp.name])

    def __init__(self, bot):
        self.bot = bot

    @commands.command('sh')
    async def prgmBash(self, ctx, *cmds):
        for log in log_proc(cmds): await ctx.send(log)

    @commands.command('py')
    async def prgmPython(self, ctx, *, code):
        python = Program.Execute('py', ['python'])
        for log in python.output(code): await ctx.send(log)

    @commands.command('js')
    async def prgmJavascript(self, ctx, *, code):
        javascript = Program.Execute('js', ['node'])
        for log in javascript.output(code): await ctx.send(log)

    @commands.command('java')
    async def prgmJava(self, ctx, *, code):
        java = Program.Execute('java', ['java'])
        for log in java.output(code): await ctx.send(log)

    @commands.command('r')
    async def prgmR(self, ctx, *, code):
        r = Program.Execute('r', ['Rscript'])
        for log in r.output(code): await ctx.send(log)


def setup(bot):
    bot.add_cog(Program(bot))
