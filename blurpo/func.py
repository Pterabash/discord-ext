import logging
import os
import random
import shelve
import subprocess
import tempfile
import textwrap
import time
from typing import List, Tuple

import requests


def database():  # -> Shelf[object]: #3.9
    return shelve.open('Database')


def rand_int_str() -> str:
    return str(random.random())[2:]


def list_attrs(obj: object, attrs: List[str]) -> str:
    return '\n'.join([f'{a}: {getattr(obj, a)}' for a in attrs])


def clamp(i: int, *, min_i: int = 1, max_i: int = 100) -> int:
    return min(max(i, min_i), max_i)


def def_url(url: str) -> str:
    GH = 'https://raw.githubusercontent.com/'
    return url if url.startswith('https://') else GH + url


def load_env(fn: str = '.env') -> None:
    f = open(fn).readlines()
    env = {(k := l.strip())[:(i := l.index('='))]: k[i+1:] for l in f}
    os.environ.update(env)


def wrap(text: str, *, width: int = 4000, lang: str = None) -> List[str]:
    ls = textwrap.wrap(text, width, replace_whitespace=False)
    return [f'```{lang}\n{s}```' for s in ls] or ['None']


def ext_path(url: str) -> Tuple[str, str]:
    path = 'ext/' + url.split('/')[-1]
    ext = path.split('.')[0].replace('/', '.')
    return path, ext


# TODO: Better alternative
def subprocess_log(args: List[str], inp: str = None) -> Tuple[str, float]:
    with tempfile.TemporaryFile('r+t') as fp:
        t = time.time()
        subprocess.run(args=args, input=inp, stdout=fp,
                       stderr=subprocess.STDOUT)
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


def error_log(e: Exception, chn_id: str) -> requests.Response:
    print(e)
    return send_embed(
        chn_id, wrap(str(e), lang='bash'),
        title=type(e).__name__, color=0xe74c3c
    )
