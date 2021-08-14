import os

from discord.ext import commands

from dscord.func import log_proc


class Program(commands.Cog):
    class Execute:
        def __init__(self, suffix: str, commands: list, *, header=None, footer=None):
            self.path = f'./script.{suffix}'
            self.file = open(self.path, 'w')
            self.commands = commands + [self.path]
            self.header = header
            self.footer = footer

        def output(self, code: str, *, x=False):
            if self.header: self.file.write(self.header+'\n')
            self.file.write(code)
            if self.footer: self.file.write(self.footer+'\n')
            self.file.close()
            if x: os.system('chmod +x '+self.file)
            logs = log_proc(self.commands)
            os.remove(self.file)
            return logs


    @commands.command('groovy')
    async def prgmGroovy(self, ctx, *, code):
        groovy = Program.Execute('groovy', ['groovy'], header='#!/usr/bin/env groovy')
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
        php = Program.Execute('php', ['php'], header='<?php', footer='?>')
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
        bash = Program.Execute('sh', [], header='#!/bin/bash')
        for log in bash.output(code, x=True): await ctx.send(log)

    @commands.command('swift')
    async def prgmSwift(self, ctx, *, code):
        swift = Program.Execute('swift', ['swift'])
        for log in swift.output(code): await ctx.send(log)


def setup(bot):
    bot.add_cog(Program())
