import random
import shelve
import subprocess
import tempfile
import textwrap
from typing import List


def clamp(val, min_val=1, max_val=100):
    return min(max(val, min_val), max_val)


def rnd_str():
    return str(random.random())[2:]


def code_wrap(txt: str, wd: int = 1950) -> List[str]:
    ls = textwrap.wrap(txt, wd, replace_whitespace=False)
    return ['```\n' + x + ' \n```' for x in ls]


def ls_attr(dic, attrs=None):
    if not attrs: attrs = dir(dic)
    ls = [f'{attr} : {getattr(dic, attr)}\n' for attr in attrs]
    return code_wrap('\n'.join(ls))


def log_proc(arg: List[str], inp=None) -> List[str]:
    with tempfile.TemporaryFile('r+t') as tp:
        subprocess.run(args=arg, input=inp, stdout=tp, stderr=subprocess.STDOUT)
        tp.seek(0)
        return code_wrap(tp.read())


class Db:
    def __init__(self, file):
        self.file = file

    def write(self, value, key=None):
        if not key: key = str(value)
        with shelve.open(self.file) as db:
            db[key] = value

    def erase(self, key):
        with shelve.open(self.file) as db:
            del db[key]

    def readkey(self):
        with shelve.open(self.file) as db:
            return [key for key in db.keys()]

    def readval(self):
        with shelve.open(self.file) as db:
            return [db[key] for key in db.keys()]
