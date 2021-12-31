import os

import blurpo


TOKEN = os.environ['TOKEN']


if __name__ == '__main__':
    blurpo.load('thisgary/blurple-o/2.0/ext/code.py')
    blurpo.run(TOKEN)
