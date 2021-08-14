import os
from tempfile import NamedTemporaryFile

from discord.ext import commands

from dscord.func import log_proc


class Program(commands.Cog):
    class Execute:
        def __init__(self, suffix: str, commands: list, 
                *, header=None, footer=None):
            self.suffix = '.' + suffix
            self.commands = commands
            self.header = header
            self.footer = footer

        def output(self, code: str):
            with NamedTemporaryFile('r+t', suffix=self.suffix) as fp:
                if self.header: fp.write(self.header+'\n')
                fp.write(code)
                if self.footer: fp.write(self.footer+'\n')
                fp.seek(0)
                return log_proc(self.commands+[fp.name])


    @commands.command('groovy')
    async def prgmGroovy(self, ctx, *, code):
        groovy = Program.Execute('groovy', ['groovy'], 
                header='#!/usr/bin/env groovy')
        for log in groovy.output(code): await ctx.send(log)

    @commands.command('js')
    async def prgmJavascript(self, ctx, *, code):
        javascript = Program.Execute('js', ['node'])
        for log in javascript.output(code): await ctx.send(log)

    @commands.command('java')
    async def prgmJava(self, ctx, *, code):
        java = Program.Execute('java', ['java'])
        for log in java.output(code): await ctx.send(log)

    @commands.command('php')
    async def prgmPhp(self, ctx, *, code):
        php = Program.Execute('php', ['php'], 
                header='<?php', footer='?>')
        for log in php.output(code): await ctx.send(log)

    @commands.command('py')
    async def prgmPython(self, ctx, *, code):
        python = Program.Execute('py', ['python'])
        for log in python.output(code): await ctx.send(log)

    @commands.command('r')
    async def prgmR(self, ctx, *, code):
        r = Program.Execute('r', ['Rscript'])
        for log in r.output(code): await ctx.send(log)

    @commands.command('ruby')
    async def prgmRuby(self, ctx, *, code):
        ruby = Program.Execute('rb', ['ruby'])
        for log in ruby.output(code): await ctx.send(log)

    @commands.command('sh')
    async def prgmBash(self, ctx, *, code):
        with open('script.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(code)
        os.system('chmod +x ./script.sh')
        for l in log_proc(['./script.sh']): await ctx.send(l)
        os.system('rm script.sh')

    @commands.command('swift')
    async def prgmSwift(self, ctx, *, code):
        swift = Program.Execute('swift', ['swift'])
        for log in swift.output(code): await ctx.send(log)


def setup(bot):
    bot.add_cog(Program())
