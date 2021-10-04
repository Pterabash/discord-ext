import os

import dscord


if __name__ == '__main__':
    if 'TOKEN' not in os.environ:
        os.environ['TOKEN'] = input('Bot token: ')
    dscord.load('code')
    dscord.load('system')
    dscord.load('whitelist')
    dscord.run(os.environ['TOKEN'])
