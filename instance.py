from urllib.request import urlopen
import os

path = 'cicada.py'
t = ''
url = 'https://raw.githubusercontent.com/cicadoves/black-tech/main/'+path
code = urlopen(url).read().decode()
open(path, 'w').write(code.replace('<token>', t))
os.system('python '+path)
