import os
import random
import shelve
import subprocess
import tempfile
import textwrap
import time
from typing import List, Tuple

import requests


API = 'https://discord.com/api/v9'


def database(): # -> Shelf[object]:
    return shelve.open('Database')


def clamp(i: int, *, min_i: int = 1, max_i: int = 100) -> int:
    return min(max(i, min_i), max_i)


def randoms() -> str:
    return str(random.random())[2:]


def list_attrs(obj: object, attrs: List[str]) -> str:
    ls = [f'{a}: {getattr(obj, a)}' for a in attrs]
    return '\n'.join(ls)


def subprocess_log(args: List[str], inp: str = None) -> Tuple[str, str]:
    with tempfile.TemporaryFile('r+t') as fp:
        t = time.time()
        subprocess.run(
            args=args, input=inp, stdout=fp, stderr=subprocess.STDOUT
        )
        dt = time.time() - t
        fp.seek(0)
        return fp.read(), dt


def wrap(text: str, *, width: int = 4000, lang: str = None) -> List[str]:
    ws = textwrap.wrap(text, width, replace_whitespace=False)
    if not ws:
        return ['No output']
    elif lang is not None:
        return [f'```{lang}\n{w}\n```' for w in ws]
    else:
        return ws


def send_embed(
    chn_id: int, chunks: List[str], *, width: int = 4000, 
    token: str = os.environ['TOKEN'], **kwargs
) -> None:
    headers = {'Authorization': f'Bot {token}'}
    json = {'embeds': []}
    for c in chunks:
        embed = {'description': c}
        embed.update(kwargs)
        json['embeds'].append(embed)
    return requests.post(
        f'{API}/channels/{chn_id}/messages', headers=headers, json=json
    )
