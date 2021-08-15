import os
from tempfile import NamedTemporaryFile
from typing import List

from discord.ext import commands

from dscord.func import sub_logs


class Program(commands.Cog):
    class Execute:
        def __init__(self, suffix: str, command: list, *,
                header: str = None, footer: str = None):
            self.suffix = '.' + suffix
            self.command = command
            self.header = header
            self.footer = footer

        def output(self, code: str) -> List[str]:
            with NamedTemporaryFile('r+t', suffix=self.suffix) as fp:
                if self.header: fp.write(self.header+'\n')
                fp.write(code)
                if self.footer: fp.write(self.footer+'\n')
                fp.seek(0)
                return sub_logs(self.command+[fp.name])


    @commands.command()
    async def groovy(self, ctx, *, code):
        groovy = Program.Execute('groovy', ['groovy'], 
                header='#!/usr/bin/env groovy')
        for log in groovy.output(code): await ctx.send(log)

    @commands.command()
    async def js(self, ctx, *, code):
        javascript = Program.Execute('js', ['node'])
        for log in javascript.output(code): await ctx.send(log)

    @commands.command()
    async def java(self, ctx, *, code):
        java = Program.Execute('java', ['java'])
        for log in java.output(code): await ctx.send(log)

    @commands.command()
    async def php(self, ctx, *, code):
        php = Program.Execute('php', ['php'], 
                header='<?php', footer='?>')
        for log in php.output(code): await ctx.send(log)

    @commands.command()
    async def py(self, ctx, *, code):
        python = Program.Execute('py', ['python'])
        for log in python.output(code): await ctx.send(log)

    @commands.command()
    async def r(self, ctx, *, code):
        r = Program.Execute('r', ['Rscript'])
        for log in r.output(code): await ctx.send(log)

    @commands.command()
    async def ruby(self, ctx, *, code):
        ruby = Program.Execute('rb', ['ruby'])
        for log in ruby.output(code): await ctx.send(log)

    @commands.command()
    async def sh(self, ctx, *, code):
        with open('script.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(code)
        os.system('chmod +x ./script.sh')
        for log in sub_logs(['./script.sh']): await ctx.send(log)
        os.system('rm script.sh')

    @commands.command()
    async def swift(self, ctx, *, code):
        swift = Program.Execute('swift', ['swift'])
        for log in swift.output(code): await ctx.send(log)


def setup(bot):
    bot.add_cog(Program())
