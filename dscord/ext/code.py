import os
from typing import List

from discord.ext import commands

from dscord.func import database, send_embed, subprocess_log, wrap


DEFAULT = {
    'py': {'args': [['python3']], 'file': {}, 'exec': {}},
    'js': {'args': [['node']], 'file': {}, 'exec': {}},
    'sh': {
        'args': [[]], 'file': {'head': '#!/bin/bash'}, 
        'exec': {'chmod': True}
    }
}


class LanguageNotFoundError(Exception):
    def __init__(self, suffix: str) -> None:
        self.message = f'Language "{suffix}" not found'
        super().__init__(self.message)


class Code(commands.Cog):
    class File:
        def __init__(
            self, suffix: str, script: str, *, head: str = None, 
            tail: str = None
        ) -> None:
            self.file = f'./foo.{suffix}'
            with open(self.file, 'w') as f:
                if head is not None:
                    f.write(f'{head}\n')
                f.write(script)
                if tail is not None:
                    f.write(f'\n{tail}')

        def exec(
            self, args: List[str] = [], *, chmod: bool = False
        ) -> None:
            if chmod:
                os.system(f'chmod +x {self.file}')
            self._logs, self._runtime = subprocess_log(args + [self.file])
            os.system(f'rm {self.file}')
        
        @property
        def logs(self):
            return self._logs
        
        @property
        def runtime(self):
            return self._runtime

    def __init__(self):
        with database() as db:
            if 'Code' not in db:
                db['Code'] = DEFAULT

    @commands.command('langadd', brief='Add language')
    async def add_language(
        self, ctx, suffix: str, args: str, *kwargs: str
    ) -> None:
        prop = {'exec': {}, 'file': {}}
        prop['args'] = [l.split(',') for l in args.split(';')]
        for i in kwargs:
            key, value = i.split('=', 1)
            if key == 'chmod':
                prop['exec']['chmod'] = True
            elif key == 'head':
                prop['file']['head'] = value
            elif key == 'tail':
                prop['file']['tail'] = value
        with database() as db:
            langs = db['Code']
            langs[suffix] = prop
            db['Code'] = langs
        send_embed(
            ctx.channel.id, ['Language added'], title='Task'
        )
    
    @commands.command('langrmv', brief='Remove language')
    async def remove_language(self, ctx, suffix: str) -> None:
        with database() as db:
            langs = db['Code']
            if suffix in langs:
                del langs[suffix]
                db['Code'] = langs
                send_embed(
                    ctx.channel.id, ['Language removed'], title='Task'
                )
            else:
                raise LanguageNotFoundError(suffix)
    
    @commands.command('langreset', brief='Reset languages')
    async def reset_languages(self, ctx):
        with database() as db:
            db['Code'] = DEFAULT
        send_embed(ctx.channel.id, ['Languages data reset'], title='Task')

    @commands.command('langs', brief='List languages')
    async def list_languages(self, ctx) -> None:
        with database() as db:
            langs = wrap('\n'.join(db['Code']), lang='bash')
            send_embed(ctx.channel.id, langs, title='Language List')
    
    @commands.command('lang', brief='Language info')
    async def get_language(self, ctx, suffix: str) -> None: 
        with database() as db:
            if suffix in db['Code']:
                text = f'suffix: {suffix}\n'
                prop = db['Code'][suffix]
                for i in prop['exec'].keys():
                    text += f'{i}: {prop["exec"][i]}\n'
                if 'file' in prop:
                    text += '\n'
                    for i in prop['file'].keys():
                        text += f'{i}: {prop["file"][i]}\n'
                chunks = wrap(text, lang=suffix)
                send_embed(ctx.channel.id, chunks, title='Language Info')
            else:
                raise LanguageNotFoundError(suffix)

    @commands.command('exec', brief='Execute script by language')
    async def exec_language(
        self, ctx, suffix: str, *, script: str
    ) -> None:
        with database() as db:
            if suffix in db['Code']:
                prop = db['Code'][suffix]
                f = Code.File(suffix, script, **prop['file'])
                for a in prop['args']:
                    f.exec(args=a, **prop['exec'])
                send_embed(
                    ctx.channel.id, wrap(f.logs, lang=suffix), title='Log', 
                    footer={'text': f'Time taken: {f.runtime}s'}
                )
            else:
                raise LanguageNotFoundError(suffix)

    @commands.command('py', brief='Execute python script')
    async def exec_python(self, ctx, *, script: str) -> None:
        f = Code.File('py', script)
        f.exec(args=['python3'])
        send_embed(
            ctx.channel.id, wrap(f.logs, lang='py'), title='Log', 
            footer={'text': f'Time taken: {f.runtime}s'}
        )


def setup(bot):
    bot.add_cog(Code())
