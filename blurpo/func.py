import random
import shelve
import subprocess
import tempfile
import textwrap
import time
from typing import List, Tuple

import requests


def database():  # -> Shelf[object]: # >=3.9
    return shelve.open('Database')


def clamp(i: int, *, min_i: int = 1, max_i: int = 100) -> int:
    return min(max(i, min_i), max_i)


def rand_int_str() -> str:
    return str(random.random())[2:]


def list_attrs(obj: object, attrs: List[str]) -> str:
    return '\n'.join([f'{a}: {getattr(obj, a)}' for a in attrs])


#TODO: Better alternative
def subprocess_log(args: List[str], inp: str = None) -> Tuple[str, float]:
    with tempfile.TemporaryFile('r+t') as fp:
        t = time.time()
        subprocess.run(args=args, input=inp, stdout=fp,
                       stderr=subprocess.STDOUT)
        dt = time.time() - t
        fp.seek(0)
        return fp.read(), dt


def wrap(text: str, *, width: int = 4000, lang: str = None) -> List[str]:
    ls = textwrap.wrap(text, width, replace_whitespace=False)
    return [f'```{lang}\n{s}```' for s in ls] or ['None']


def send_embed(channel_id: int, token: str,
               chunks: List[str], **fields) -> requests.Response:
    return requests.post(
        f'https://discord.com/api/v9/channels/{channel_id}/messages',
        headers={'Authorization': f'Bot {token}'},
        json={'embeds': [{**{'description': c}, **fields} for c in chunks]}
        # json={'embeds': [{'description': c} | fields for c in chunks]} # >=3.9
    )


def error_logs(e: Exception, channel_id: str, token: str):
    print(e)
    send_embed(
        channel_id, token, wrap(str(e), lang='bash'),
        title=type(e).__name__, color=0xe74c3c
    )
