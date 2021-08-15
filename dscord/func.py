import random
import shelve
import subprocess
import tempfile
import textwrap
from typing import List


def clamp(i: int, min_int: int = 1, max_int:int = 100) -> int:
    return min(max(i, min_int), max_int)


def rng_str() -> str:
    return str(random.random())[2:]


def code_wrap(txt: str, width: int = 1950) -> List[str]:
    lines = textwrap.wrap(txt, width, replace_whitespace=False)
    return [f'```\n{l}\n```' for l in lines]


def dict_wrap(d: dict, keys: List[str] = None) -> List[str]:
    if not keys: keys = dir(d)
    keyvals = [f'{key}: {getattr(d, key)}' for key in keys]
    return code_wrap('\n\n'.join(keyvals))


def sub_logs(args: List[str], inp: str = None) -> List[str]:
    with tempfile.TemporaryFile('r+t') as fp:
        subprocess.run(args=args, input=inp, stdout=fp, stderr=subprocess.STDOUT)
        fp.seek(0)
        return code_wrap(fp.read())


class Db:
    def __init__(self, name):
        self.name = name

    def write(self, value, key=None):
        if not key: key = str(value)
        with shelve.open(self.name) as db:
            db[key] = value

    def erase(self, key):
        with shelve.open(self.name) as db:
            del db[key]

    def keys(self):
        with shelve.open(self.name) as db:
            return list(db)

    def vals(self):
        with shelve.open(self.name) as db:
            return [db[key] for key in db.keys()]
