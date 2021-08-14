import os

from discord.ext import commands

from dscord.func import log_proc


class Program(commands.Cog):
    class Execute:
        def __init__(self, suffix: str, commands: list, *, header=None):
            self.file = f'file.{suffix}'
            self.commands = commands+[self.file]
            self.header = header

        def output(self, code: str, *, x=False):
            with open(self.file, 'w') as f:
                if self.header: f.write(f'{self.header}\n')
                f.write(code)
            if x:
                os.system('chmod +x ./'+self.file)
                logs = log_proc(['./'+self.file])
            else: 
                logs = log_proc(self.commands)
            os.remove(self.file)
            return logs


    def __init__(self, bot):
        self.bot = bot

    @commands.command('sh')
    async def prgmBash(self, ctx, *, code):
        bash = Program.Execute('sh', [], header='#!/bin/bash')
        for log in bash.output(code, x=True): await ctx.send(log)

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
