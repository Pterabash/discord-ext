import os
from pathlib import Path
from typing import List

from discord.ext import commands

from blurpo.func import EvalFile, send_embed, subprocess_log, wrap


DEFAULT = {
    'py': {'args': [['python']]},
    'js': {'args': [['node']]},
    'sh': {'args': [[]], 'tags': ['x'],
           'code': {'hd': '#!/bin/bash'}}
}
TAGS = ['x']
KEYS = ['hd', 'tl']
lang = EvalFile('code')


class LangNotFoundError(Exception):
    def __init__(self, suff: str) -> None:
        self.message = f'Language "{suff}" not found'
        super().__init__(self.message)


class Code(commands.Cog):
    @staticmethod
    def write(name: str, code: str, *,
              hd: str = None, tl: str = None) -> None:
        with open(name, 'w') as f:
            not hd or f.write(hd + '\n')
            f.write(code)
            not tl or f.write('\n' + tl)

    @staticmethod
    def exec(name: str, args: List[str] = [], *tags) -> None:
        try:
            'x' in tags and os.system('xhmod +x ' + name)
            return subprocess_log(args + [name])
        except:
            raise
        finally:
            os.remove(name)

    @staticmethod
    def output(channel_id: int, log: str, t: float) -> None:
        send_embed(channel_id, wrap(log), title='Output',
                   footer={'text': f'Runtime: {t}s'})

    def __init__(self):
        Path('exts.eval').exists() or EvalFile('exts', init=True, val=set())

    @commands.command('ladd', brief='Add lang')
    async def add_lang(self, ctx, suff: str, cmds: str, *args: str) -> None:
        prop = {'tags': [], 'code': {}}
        prop['args'] = [a.split(',') for a in cmds.split(';')]
        for arg in args:
            if arg in TAGS:
                prop['tags'].append(arg)
            else:
                k, v = arg.split('=', 1)
                if k in KEYS:
                    prop['code'][k] = v
            lang.update({suff: prop})
        send_embed(ctx.channel.id, ['Language added'], title='Task')

    @commands.command('lrmv', brief='Remove lang')
    async def rmv_lang(self, ctx, suff: str) -> None:
        if suff not in lang.get():
            raise LangNotFoundError(suff)
        lang.delete(suff)
            
    @commands.command('linit', brief='Reset langs')
    async def reset_langs(self, ctx):
        lang.set(DEFAULT)
        send_embed(ctx.channel.id, ['Reset'], title='Languages')

    @commands.command('langs', brief='List langs')
    async def list_langs(self, ctx) -> None:
        log = '\n'.join(lang.get(list))
        send_embed(ctx.channel.id, wrap(log), title='Languages')

    @commands.command('lang', brief='Lang info')
    async def get_lang(self, ctx, suff: str) -> None:
        log = f'suffix: {suff}\n'
        l = lang.get()
        if suff not in l:
            raise LangNotFoundError(suff)
        prop = l[suff]
        for k in prop:
            log += f'{k}: {prop[k]}\n'
        send_embed(ctx.channel.id, wrap(log), title='Language')

    @commands.command('exec', brief='Exec code by lang')
    async def exec_lang(self, ctx, suff: str, *, code: str) -> None:
        name = 'foo.' + suff
        l = lang.get()
        if suff not in l:
            raise LangNotFoundError(suff)
        prop = l[suff]
        Code.write(name, code, **prop['code'])
        for args in prop['args']:
            log, t = Code.exec(name, args, *prop['tags'])
        Code.output(ctx.channel.id, log, t)
                

    @commands.command('py', brief='Exec python code')
    async def exec_python(self, ctx, *, code: str) -> None:
        NAME = 'foo.py'
        Code.write(NAME, code)
        Code.output(ctx.channel.id, *Code.exec(NAME, ['python']))


def setup(bot):
    bot.add_cog(Code())
