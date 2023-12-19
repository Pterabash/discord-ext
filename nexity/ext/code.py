import os
from pathlib import Path
from typing import List

from discord.ext import commands

from nexity.util import load_data, save_data, send_embeds, subprocess_log, wrap


# constants
DEFAULT = {
    'py': {'args': [['python']], 'kwargs': {}},
    'js': {'args': [['node']], 'kwargs': {}},
    'sh': {'args': [[]], 'kwargs': {'hd': '#!/bin/bash', 'x': True}}
}
TAGS = ['x']
KEYS = ['hd', 'tl']

# variables
data = load_data(languages=DEFAULT)
lang = data['languages']


class LangNotFoundError(Exception):
    def __init__(self, suffix: str) -> None:
        self.message = f'Language "{suffix}" not found'
        super().__init__(self.message)


class Exec:
    def __init__(self, suffix: str, code: str, *, 
                 hd: str = None, tl: str = None, x: bool = False) -> None:
        if hd:
            code = f'{hd}\n' + code
        if tl:
            code += f'\n{tl}'
        self.name = f'code/foo.{suffix}'
        path = Path(self.name)
        path.write_text(code)
        x and path.chmod(0o777)

    def exec(self, chn_id: int, argss: List[List[str]] = [], *, 
             cleanup: bool = False) -> None:
        for args in argss:
            try:
                log, t = subprocess_log(args + [self.name])
                send_embeds(chn_id, wrap(log), title='Output', 
                            footer={'text': f'Runtime: {t}s'})
            finally:
                cleanup and os.remove(self.name)


class Code(commands.Cog):
    @commands.command('ladd', brief='Add lang')
    async def add_lang(self, ctx, suffix: str, args: str, *kwargs: str) -> None:
        prop = {'kwargs': {}}
        prop['args'] = [a.split(',') for a in args.split(';')]
        for kw in kwargs:
            if '=' in kw:
                key, val = kw.split('=', 1)
                prop['code'][key] = val
            else:
                prop['kwargs'][kw] = True
            lang[suffix] = prop
        save_data(data, languages=lang)
        send_embeds(ctx.channel.id, ['Language added'], title='Language')

    @commands.command('lrmv', brief='Remove lang')
    async def rmv_lang(self, ctx, suffix: str) -> None:
        if suffix not in lang:
            raise LangNotFoundError(suffix)
        del lang[suffix]
        save_data(data, languages=lang)
            
    @commands.command('linit', brief='Reset langs')
    async def reset_langs(self, ctx):
        lang = DEFAULT
        save_data(data, languages=lang)
        send_embeds(ctx.channel.id, ['Reset'], title='Languages')

    @commands.command('langs', brief='List langs')
    async def list_langs(self, ctx) -> None:
        log = '\n'.join(lang.keys())
        send_embeds(ctx.channel.id, wrap(log), title='Languages')

    @commands.command('lang', brief='Lang info')
    async def get_lang(self, ctx, suffix: str) -> None:
        log = f'suffix: {suffix}\n'
        if suffix not in lang:
            raise LangNotFoundError(suffix)
        prop = lang[suffix]
        for k in prop:
            log += f'{k}: {prop[k]}\n'
        send_embeds(ctx.channel.id, wrap(log), title='Language')

    @commands.command('exec', brief='Exec code by lang')
    async def exec_lang(self, ctx, suffix: str, *, code: str) -> None:
        if suffix not in lang:
            raise LangNotFoundError(suffix)
        prop = lang[suffix]
        code = Exec(suffix, code, **prop['kwargs'])
        code.exec(ctx.channel.id, prop['args'])

    @commands.command('py', brief='Exec python code')
    async def exec_python(self, ctx, *, code: str) -> None:
        prop = lang['py']
        code = Exec('py', code, **prop['kwargs'])
        code.exec(ctx.channel.id, prop['args'])


async def setup(bot):
    Path('code').mkdir(exist_ok=True)
    await bot.add_cog(Code())
