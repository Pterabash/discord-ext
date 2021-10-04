import os
from typing import List

from discord.ext import commands

from dscord.func import database, send_embed, subprocess_log, wrap


DEFAULT = {
    'py': {
        'args': [['python3']]
    },
    'js': {
        'args': [['node']]
    },
    'sh': {
        'args': [[]],
        'head': '#!/bin/bash',
        'chmod': True
    }
}


class Code(commands.Cog):
    class File:
        def __init__(
            self, suffix: str, code: str, *, head: str = None, 
            tail: str = None, **kwargs
        ) -> None:
            self.base = f'./foo.{suffix}'
            with open(self.base, 'w') as f:
                if head is not None:
                    f.write(f'{head}\n')
                f.write(code)
                if tail is not None:
                    f.write(f'\n{tail}')

        def exec(
            self, args: List[str] = [], *, chmod: bool = False, **kwargs
            # Considering better solution
        ) -> List[str]:
            if chmod:
                os.system(f'chmod +x {self.base}')
            log = subprocess_log(args + [self.base])
            os.system(f'rm {self.base}')
            return log


    def __init__(self):
        with database() as db:
            if 'Code' not in db:
                db['Code'] = DEFAULT

    @commands.command()
    async def add_language(self, ctx, suffix: str, *args: str) -> None:
        prop = {}
        for a in args:
            if a.startswith('args='):
                prop['args'] = [
                    i.split(',') for i in a.split('=')[1].split(';')
                ]
            elif a.startswith('head='):
                prop['head'] = a.split('=')[1]
            elif a.startswith('tail='):
                prop['tail'] = a.split('=')[1]
        with database() as db:
            db['Code'][suffix] = prop
        await ctx.send('Database updated')
    
    @commands.command('run', brief='Run script by language')
    async def run_script(self, ctx, suffix: str, *, script: str) -> None:
        with database() as db:
            if suffix in db['Code']:
                prop = db['Code'][suffix]
                f = Code.File(suffix, **prop)
                log = f.exec(**prop)
                send_embed(ctx.channel.id, wrap(log, lang=suffix))
            else:
                await ctx.send('Language not found')

    # @commands.command()
    # async def groovy(self, ctx, *, code: str) -> None:
    #     groovy = Code.File('groovy', code, head='#!/usr/bin/env groovy')
    #     groovy.execute(['groovy'])

    # @commands.command()
    # async def js(self, ctx, *, code) -> None:
    #     javascript = Code.File('js', code)
    #     logs = javascript.execute(['node'])

    # @commands.command()
    # async def java(self, ctx, *, code: str) -> None:
    #     java = Code.Execute('java', code)
    #     logs = java.execute(['java'])

    # @commands.command()
    # async def php(self, ctx, *, code: str) -> None:
    #     php = Code.File('php', code, head='<?php', tail='?>')
    #     logs = php.execute(['pfp'])

    # @commands.command()
    # async def py(self, ctx, *, code: str) -> None:
    #     python = Code.File('py', code)
    #     logs = python.execute(['python3'])

    # @commands.command()
    # async def r(self, ctx, *, code: str) -> None:
    #     r = Code.File('r', code)
    #     logs = r.execute(['Rscript'])

    # @commands.command()
    # async def ruby(self, ctx, *, code: str) -> None:
    #     ruby = Code.File('rb', code)
    #     logs = ruby.execute(['ruby'])

    # @commands.command()
    # async def sh(self, ctx, *, code: str) -> None:
    #     bash = Code.File('sh', code,
    #             head='#!/bin/bash')
    #     bash.chmod()
    #     logs = bash.execute()

    # @commands.command()
    # async def swift(self, ctx, *, code: str) -> None:
    #     swift = Code.File('swift', code)
    #     logs = swift.execute(['swift'])


def setup(bot):
    bot.add_cog(Code())
