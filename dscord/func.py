import os
import random
import shelve
import subprocess
import tempfile
import textwrap
from typing import List, Shelf

import requests


API = 'https://discord.com/api/v9'


def database() -> Shelf[object]:
    return shelve.open('Database')


def clamp(i: int, *, min: int = 1, max: int = 100) -> int:
    return min(max(i, min), max)


def rng_str() -> str:
    return str(random.random())[2:]


def code_wrap(txt: str, width: int = 1950) -> List[str]:
    lines = textwrap.wrap(txt, width, replace_whitespace=False)
    return [f'```\n{l}\n```' for l in lines]


def dict_wrap(d: dict, keys: List[str] = None) -> List[str]:
    if not keys: 
        keys = dir(d)
    keyvals = [f'{key} : {d[key]}' for key in keys]
    return code_wrap('\n\n'.join(keyvals))


def sub_logs(args: List[str], inp: str = None) -> List[str]:
    with tempfile.TemporaryFile('r+t') as fp:
        subprocess.run(
            args=args, 
            input=inp, 
            stdout=fp, 
            stderr=subprocess.STDOUT
        )
        fp.seek(0)
        return code_wrap(fp.read())


def send_embed(
    chn_id: str, txt: str, width: int = 4000, *, title: str = None
) -> None:
    headers = {'Authorization': f'Bot {os.environ["TOKEN"]}'}
    json = {'embeds': []}
    embed = {'title': title}
    wrap = textwrap.wrap(txt, width, replace_whitespace=False)
    for w in wrap:
        embed['description'] = f'```py\n{w}\n```'
        json['embeds'].append(embed)
    requests.post(
        f'{API}/channels/{chn_id}/messages', 
        headers=headers, 
        json=json
    )
