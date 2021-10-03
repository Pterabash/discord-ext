import os
import random
import shelve
import subprocess
import tempfile
import textwrap
from typing import List

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


def send_embed(
    chn_id: int, text: str, *, title: str = None, width: int = 4000, 
    token: str = os.environ['TOKEN']
) -> None:
    headers = {'Authorization': f'Bot {token}'}
    wrap = textwrap.wrap(text, width, replace_whitespace=False)
    json = {'embeds': [{'title': title, 'description': w} for w in wrap]}
    return requests.post(
        f'{API}/channels/{chn_id}/messages', headers=headers, json=json
    )


def error_log(f: callable) -> callable:
    def fx():
        try:
            f()
        except Exception as e:
            print(e)
    return fx


# Deprecated
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
            args=args, input=inp, stdout=fp, stderr=subprocess.STDOUT
        )
        fp.seek(0)
        return code_wrap(fp.read())