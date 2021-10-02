import os

import dscord


if __name__ == '__main__':
    dscord.load('system')
    dscord.load('whitelist')
    token = os.getenv('TOKEN')
    if not token:
        token = input('Bot token: ')
    dscord.run(token)