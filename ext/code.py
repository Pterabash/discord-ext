import os
import sys
from typing import List

from discord.ext import commands

from blurpo.func import database, send_embed, subprocess_log, wrap


DEFAULT = {
    'py': {'args': [['python']]},
    'js': {'args': [['node']]},
    'sh': {'args': [[]], 'tags': ['chmod'],
           'file': {'head': '#!/bin/bash'}}
}
TAGS = ['chmod']
KEYS = ['head', 'tail']


class LangNotFoundError(Exception):
    def __init__(self, suffix: str) -> None:
        self.message = f'Language "{suffix}" not found'
        super().__init__(self.message)


class Code(commands.Cog):
    class File:
        def __init__(self, suffix: str, script: str, *,
                     head: str = None, tail: str = None) -> None:
            self.file = f'./foo.{suffix}'
            with open(self.file, 'w') as f:
                if head is not None:
                    f.write(f'{head}\n')
                f.write(script)
                if tail is not None:
                    f.write(f'\n{tail}')

        def exec(self, args: List[str] = [], *,
                 chmod: bool = False) -> None:
            if chmod:
                os.system(f'chmod +x {self.file}')
            self._logs, self._runtime = subprocess_log(args + [self.file])
            rm = 'del' if sys.platform == 'win32' else 'rm'
            os.system(f'{rm} {self.file}')

        @property
        def logs(self): return self._logs

        @property
        def runtime(self): return self._runtime

    def __init__(self, bot):
        self.bot = bot
        with database() as db:
            if 'Code' not in db:
                db['Code'] = DEFAULT

    @commands.command('langadd', brief='Add language')
    async def add_language(self, ctx, suffix: str,
                           commands: str, *args: str) -> None:
        prop = {'args': [], 'tags': [], 'file': {}}
        prop['args'] = [l.split(',') for l in commands.split(';')]
        for arg in args:
            if arg in TAGS:
                prop['tags'].append(arg)
            else:
                key, value = arg.split('=', 1)
                if key in KEYS:
                    prop['file'][key] = value
        with database() as db:
            langs = db['Code']
            langs[suffix] = prop
            db['Code'] = langs
        send_embed(ctx.channel.id, ['Language added'], title='Task')

    @commands.command('langrmv', brief='Remove language')
    async def remove_language(self, ctx, suffix: str) -> None:
        with database() as db:
            langs = db['Code']
            if suffix in langs:
                del langs[suffix]
                db['Code'] = langs
                send_embed(ctx.channel.id, ['Language removed'],
                           title='Task')
            else:
                raise LangNotFoundError(suffix)

    @commands.command('langreset', brief='Reset languages')
    async def reset_languages(self, ctx):
        with database() as db:
            db['Code'] = DEFAULT
        send_embed(ctx.channel.id, ['Languages reset'], title='Task')

    @commands.command('langs', brief='List languages')
    async def list_languages(self, ctx) -> None:
        with database() as db:
            langs = wrap('\n'.join(db['Code']), lang='')
            send_embed(ctx.channel.id, langs, title='Language List')

    @commands.command('lang', brief='Language info')
    async def get_language(self, ctx, suffix: str) -> None:
        with database() as db:
            if suffix in db['Code']:
                prop = db['Code'][suffix]
                text = f'suffix: {suffix}\nargs: {prop["args"]}\n'
                for k in prop:
                    if type(j := prop[k]) is dict:
                        l = '\n'.join([f'{i}: {j[i]}' for i in j])
                        text += f'\n{k}\n{l}\n'
                chunks = wrap(text, lang='')
                send_embed(ctx.channel.id, chunks, title='Language Info')
            else:
                raise LangNotFoundError(suffix)

    @commands.command('exec', brief='Execute script by language')
    async def exec_language(self, ctx, suffix: str, *, script: str) -> None:
        with database() as db:
            if suffix in db['Code']:
                prop = db['Code'][suffix]
                f = Code.File(suffix, script, **prop['file'])
                for d in prop['args']:
                    f.exec(args=d, **prop['exec'])
                send_embed(
                    ctx.channel.id, wrap(f.logs, lang=''), title=f'Log ({suffix})',
                    footer={'text': f'Time taken: {f.runtime}s'}
                )
            else:
                raise LangNotFoundError(suffix)

    @commands.command('py', brief='Execute python script')
    async def exec_python(self, ctx, *, script: str) -> None:
        # f = Code.File('py', script)
        # f.exec(args=['python'])
        # send_embed(
        #     ctx.channel.id, wrap(f.logs, lang=''), title='Log (py)',
        #     footer={'text': f'Time taken: {f.runtime}s'}
        # )
        await ctx.invoke(self.bot.get_command('exec'), 'py', script)


def setup(bot):
    bot.add_cog(Code(bot))
