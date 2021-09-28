import os
from typing import List

from discord.ext import commands
from dscord.func import sub_logs


class Program(commands.Cog):
    class File:
        def __init__(self, suffix: str, code: str, 
                *, header: str = None, footer: str = None) -> None:
            self.base = f'file.{suffix}'
            with open(self.base, 'w') as f:
                if header: f.write(f'{header}\n')
                f.write(code)
                if footer: f.write(f'\n{footer}')
            self.base = f'./{self.base}'

        def chmod(self) -> None:
            os.system(f'chmod +x {self.base}')

        def execute(self, args: List[str] = []) -> List[str]:
            logs = sub_logs(args + [self.base])
            os.system(f'rm {self.base}')
            return logs


    @commands.command()
    async def groovy(self, ctx, *, code: str) -> None:
        groovy = Program.File('groovy', code, 
                header='#!/usr/bin/env groovy')
        logs = groovy.execute(['groovy'])
        for log in logs: await ctx.send(log)

    @commands.command()
    async def js(self, ctx, *, code) -> None:
        javascript = Program.File('js', code)
        logs = javascript.execute(['node'])
        for log in logs: await ctx.send(log)

    @commands.command()
    async def java(self, ctx, *, code: str) -> None:
        java = Program.Execute('java', code)
        logs = java.execute(['java'])
        for log in logs: await ctx.send(log)

    @commands.command()
    async def php(self, ctx, *, code: str) -> None:
        php = Program.File('php', code, 
                header='<?php', footer='?>')
        logs = php.execute(['pfp'])
        for log in logs: await ctx.send(log)

    @commands.command()
    async def py(self, ctx, *, code: str) -> None:
        python = Program.File('py', code)
        logs = python.execute(['python3'])
        for log in logs: await ctx.send(log)

    @commands.command()
    async def r(self, ctx, *, code: str) -> None:
        r = Program.File('r', code)
        logs = r.execute(['Rscript'])
        for log in logs: await ctx.send(log)

    @commands.command()
    async def ruby(self, ctx, *, code: str) -> None:
        ruby = Program.File('rb', code)
        logs = ruby.execute(['ruby'])
        for log in logs: await ctx.send(log)

    @commands.command()
    async def sh(self, ctx, *, code: str) -> None:
        bash = Program.File('sh', code,
                header='#!/bin/bash')
        bash.chmod()
        logs = bash.execute()
        for log in logs: await ctx.send(log)

    @commands.command()
    async def swift(self, ctx, *, code: str) -> None:
        swift = Program.File('swift', code)
        logs = swift.execute(['swift'])
        for log in logs: await ctx.send(log)


def setup(bot):
    bot.add_cog(Program())
