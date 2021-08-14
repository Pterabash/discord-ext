import os
import dscord

if __name__ == '__main__':
    dscord.load('system')
    dscord.run(os.environ['TOKEN'])

