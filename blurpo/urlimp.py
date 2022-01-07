from importlib import import_module
from pathlib import Path
from urllib.request import urlopen


def basename(url: str) -> str:
    return url.split('#')[0].split('?')[0].split('/')[-1].split('.')[0]


def import_url(url: str, *, path: str = 'mdl', filename: str = None):
    code = str(urlopen(url).read().decode())
    _path = Path(path)
    _path.mkdir(parents=True, exist_ok=True)
    name = filename or basename(url)
    _file = _path / (name + '.py')
    _file.write_text(code)
    package = path.replace('/', '.')
    return import_module('.' + name, package)
