from pathlib import Path


class fdict(dict):
    def __init__(self, *args, **kwargs):
        keyword = lambda k, v : (kwargs.pop(k) if k in kwargs else v)
        path = keyword('_path', '.dict') 
        init = keyword('_init', False) 
        self.__path__ = Path(path)
        if self.__path__.exists() and not init:
            kwargs = eval(self.__path__.read_text())
        super(fdict, self).__init__(*args, **kwargs)
        self.write()

    @staticmethod
    def read(path: str = '.dict') -> dict: 
        _path = Path(path)
        return _path.exists() and fdict(eval(_path.read_text()), _path=path)

    def write(self) -> None:
        Path(self.__path__).write_text(str(self))

    @property
    def path(self) -> str:
        return self.__path__

    @path.setter
    def path(self, new_path: str) -> None:
        self.__path__.rename(new_path)
