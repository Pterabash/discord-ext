import os

from .bot import load_ext, load_url, prefix, run
from .func import database, load_env


__all__ = ['load_ext', 'load_url', 'prefix', 'run', 'load_env']

if not os.path.isdir('exts'):
    os.mkdir('exts')

with database() as db:
    if 'Extension' not in db:
        db['Extension'] = {'local': [], 'remote': []}
