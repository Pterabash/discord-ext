import random
import shelve
import tempfile
import textwrap
import subprocess

def clamp(val, min_val=1, max_val=100):
    return min(max(val, min_val), max_val)

def rnd_str():
    return str(random.random())[2:]

def code_wrap(txt, wd=1950):
    ls = textwrap.wrap(txt, wd,
            break_long_words=False, replace_whitespace=False)
    return ['```\n'+x+' \n```' for x in ls]

def ls_attr(dic, attrs=None):
    if not attrs: attrs = dir(dic)
    ls = [f'{attr} : {getattr(dic, attr)}\n' for attr in attrs]
    return code_wrap('\n'.join(ls))

def log_proc(arg, inp=None):
    with tempfile.TemporaryFile('r+t') as tp:
        subprocess.run(args=arg,input=inp,stdout=tp,stderr=subprocess.STDOUT)
        tp.seek(0)
        return code_wrap(tp.read())


class Db:
    def __init__(self, file):
        self.file = file

    def write(self, key, value=None):
        if not value: value = key
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

