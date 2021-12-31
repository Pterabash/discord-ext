import os

import blurpo


if __name__ == '__main__':
    if 'TOKEN' not in os.environ:
        os.environ['TOKEN'] = input('Bot token: ')
    blurpo.load('thisgary/blurple-o/main/ext/code.py')
    blurpo.load('thisgary/blurple-o/main/ext/whitelist.py')
    blurpo.run(os.environ['TOKEN'])
