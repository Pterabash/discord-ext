import os
import sys
from typing import List

from discord.ext import commands

from dscord.func import database, send_embed, subprocess_log, wrap


DEFAULT = {
    'py': {'file': {}, 'exec': {'args': [['python3']]}},
    'js': {'file': {}, 'exec': {'args': [['node']]}},
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
                os.system(f'chmod +x {self.base}')
            log, t = subprocess_log(args + [self.base])
            os.system(f'rm {self.base}')
            return log, t


    def __init__(self):
        with database() as db:
            if 'Code' not in db:
                db['Code'] = DEFAULT

    @commands.command('langadd', brief='Add language')
    async def add_language(self, ctx, suffix: str, *args: str) -> None:
        prop = {'exec': {}, 'file': {}}
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
            langs = db['Code']
            langs[suffix] = prop
            db['Code'] = langs
        await ctx.send('Language added')

    @commands.command('langs', brief='List languages')
    async def list_languages(self, ctx) -> None:
        with database() as db:
            chunks = wrap('\n'.join(db['Code'].keys()))
            send_embed(
                ctx.channel.id, chunks, lang='bash', title='Language List'
            )
    
    @commands.command('lang', brief='Language info')
    async def get_language_info(self, ctx, suffix: str) -> None: 
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
                send_embed(
                    ctx.channel.id, 'Language not found', title='Error'
                )

    @commands.command('exec', brief='Execute script by language')
    async def exec_script(self, ctx, suffix: str, *, script: str) -> None:
        with database() as db:
            if suffix in db['Code']:
                prop = db['Code'][suffix]
                f = Code.File(suffix, script, **prop['file'])
                for args in prop['exec'].pop('args'):
                    log, t = f.exec(args=args, **prop['exec'])
                send_embed(
                    ctx.channel.id, wrap(log, lang=suffix), title='Output',
                    footer={'text': f'Time taken: {t}s'}
                )
            else:
                send_embed(
                    ctx.channel.id, 'Language not found', title='Error'
                )


def setup(bot):
    bot.add_cog(Code())
