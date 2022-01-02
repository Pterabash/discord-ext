from contextlib import contextmanager
import os
import random
import subprocess
import tempfile
import textwrap
import time
from typing import List, Tuple

import requests


GH = 'https://raw.githubusercontent.com/'


class EvalFile:
    @staticmethod
    def read(var: str) -> any:
        return eval(open('.' + var).read())

    @staticmethod
    def write(var: str, val: any = None) -> any:
        if type(val) is str:
            raise Exception("Argument 'val' can't be str")
        open('.' + var, 'w').write(str(val))

    def __init__(self, var: str = 'eval', *, val: any = None) -> None:
        self.var = var
        EvalFile.write(var, val)

    def get(self) -> any:
        return EvalFile.read(self.var)

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


def rand_int_str() -> str:
    return str(random.random())[2:]


def basename(path: str) -> str:
    return path.split('/')[-1].split('.')[0]


def list_attrs(obj: object, attrs: List[str]) -> str:
    return '\n'.join([f'{a}: {getattr(obj, a)}' for a in attrs])


def repo_check(path: str) -> str:
    return path.startswith('https://') and path or GH + path


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


def error_log(e: Exception, chn_id: int = None) -> requests.Response:
    log = f'{type(e).__name__}: {e}'
    print(log)
    return chn_id and send_embed(
        chn_id, wrap(log, lang='bash'),
        title='Error', color=0xe74c3c
    )


@contextmanager
def try_log(chn_id: int):
    try:
        yield
    except Exception as e:
        error_log(e, chn_id)
