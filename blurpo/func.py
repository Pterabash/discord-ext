import logging
import os
from pathlib import Path
import random
import subprocess
import tempfile
import textwrap
import time
from typing import List, Tuple

import requests


class EvalFile:
    @staticmethod
    def read(var: str, *, f: callable = None) -> any:
        val = eval(open(var + '.eval').read())
        return f(val) if f else val

    @staticmethod
    def write(var: str, val: any = None) -> any:
        if type(val) is str:
            raise Exception("Argument 'val' can't be str")
        open(var + '.eval', 'w').write(str(val))

    def __init__(self, var: str = 'eval', *, val: any = None) -> None:
        self.var = var
        Path(var + '.eval').exists() or self.set(val)

    def get(self, *, f: callable = None) -> any:
        return EvalFile.read(self.var, f=f)

    def set(self, val: any) -> any:
        EvalFile.write(self.var, val)
        return self.get()

    def add(self, val: any) -> set:
        _val = self.get()
        _val.add(val)
        return self.set(_val)
    
    def discard(self, val: any) -> set:
        _val = self.get()
        _val.discard(val)
        return self.set(_val)
    
    def update(self, d: dict) -> dict:
        _val = self.get()
        _val.update(d)
        return self.set(_val)
    
    def delete(self, key: str) -> dict:
        _val = self.get()
        del _val[key]
        return self.set(_val)
    
    def append(self, val: any) -> list:
        _val = self.get()
        _val.append(val)
        return self.set(_val)


def rand_int_str() -> str:
    return str(random.random())[2:]


def basename(path: str) -> str:
    return path.split('/')[-1].split('.')[0]


def list_attrs(obj: object, attrs: List[str]) -> str:
    return '\n'.join([f'{a}: {getattr(obj, a)}' for a in attrs])


def clamp(i: int, *, min_i: int = 1, max_i: int = 100) -> int:
    return min(max(i, min_i), max_i)


def load_env(fn: str = '.env') -> None:
    f = open(fn).readlines()
    env = {(k := l.strip())[:(i := l.index('='))]: k[i+1:] for l in f}
    os.environ.update(env)


def wrap(text: str, *, width: int = 4000, lang: str = None) -> List[str]:
    ls = textwrap.wrap(text, width, replace_whitespace=False)
    return [f'```{lang}\n{s}```' for s in ls] or ['None']


# TODO: Better alternative
def subprocess_log(args: List[str], inp: str = None) -> Tuple[str, float]:
    with tempfile.TemporaryFile('r+t') as fp:
        t = time.time()
        subprocess.run(
            args=args, input=inp, stdout=fp, stderr=subprocess.STDOUT
        )
        dt = time.time() - t
        fp.seek(0)
        return fp.read(), dt


def send_embed(chn_id: int, chunks: List[str], **fields) -> requests.Response:
    return requests.post(
        f'https://discord.com/api/v9/channels/{chn_id}/messages',
        headers={'Authorization': f'Bot {os.environ["TOKEN"]}'},
        json={'embeds': [{**{'description': c}, **fields} for c in chunks]}
        # json={'embeds': [{'description': c} | fields for c in chunks]} #3.9
    )


def error_log(e: Exception, chn_id: int) -> requests.Response:
    logging.exception(e)
    return chn_id and send_embed(
        chn_id, wrap(str(e), lang='bash'),
        title=type(e).__name__, color=0xe74c3c
    )
