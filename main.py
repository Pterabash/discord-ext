import os

import blurpo


if __name__ == '__main__':
    if 'TOKEN' not in os.environ:
        os.environ['TOKEN'] = input('Bot token: ')
    blurpo.load('code')
    blurpo.load('system')
    blurpo.load('whitelist')
    blurpo.run(os.environ['TOKEN'])
