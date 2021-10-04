import os
from typing import List

from discord.ext import commands

from dscord.func import database, send_embed, subprocess_log, wrap


DEFAULT = {
    'py': {'exec': {'args': [['python3']]}},
    'js': {'exec': {'args': [['node']]}},
    'sh': {
        'file': {'head': '#!/bin/bash'}, 
        'exec': {'args': [[]], 'chmod': True}
    }
}


class Code(commands.Cog):
    class File:
        def __init__(
            self, suffix: str, script: str, *, head: str = None, 
            tail: str = None
        ) -> None:
            self.base = f'./foo.{suffix}'
            with open(self.base, 'w') as f:
                if head is not None:
                    f.write(f'{head}\n')
                f.write(script)
                if tail is not None:
                    f.write(f'\n{tail}')

        def exec(
            self, args: List[str] = [], *, chmod: bool = False
        ) -> List[str]:
            if chmod:
                subprocess_log(['chmod', '+x', self.base])
            log, t = subprocess_log(args + [self.base])
            subprocess_log(['rm', self.base])
            return log, t


    def __init__(self):
        with database() as db:
            if 'Code' not in db:
                db['Code'] = DEFAULT

    @commands.command()
    async def add_language(self, ctx, suffix: str, *args: str) -> None:
        prop = {}
        for a in args:
            if a.startswith('args='):
                prop['exec']['args'] = [
                    i.split(',') for i in a.split('=')[1].split(';')
                ]
            elif a.startswith('chmod='):
                val = a.split('=')[1]
                if val.lower() == 'true':
                    prop['exec']['chmod'] = True
                elif val.lower() == 'false':
                    prop['exec']['chmod'] = False
            elif a.startswith('head='):
                prop['file']['head'] = a.split('=')[1]
            elif a.startswith('tail='):
                prop['file']['tail'] = a.split('=')[1]
        with database() as db:
            db['Code'][suffix] = prop
        await ctx.send('Database updated')

    @commands.command('langs', brief='List languages')
    async def list_languages(self, ctx) -> None:
        with database() as db:
            send_embed(
                ctx.channel.id, wrap(str(db['Code']), lang='bash'), 
                title='Language List'
            )

    @commands.command('exec', brief='Execute script by language')
    async def exec_script(self, ctx, suffix: str, *, script: str) -> None:
        with database() as db:
            if suffix in db['Code']:
                prop = db['Code'][suffix]
                if 'file' in prop:
                    f = Code.File(suffix, script, prop['file'])
                else:
                    f = Code.File(suffix, script)
                for args in prop['exec'].pop('args'):
                    log, t = f.exec(args=args, **prop['exec'])
                send_embed(
                    ctx.channel.id, 
                    wrap(log, lang=suffix),
                    title='Output',
                    footer=f'Time taken: {t}s'
                )
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
