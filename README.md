# descordlib

Discord.py related library.

## Installation

    pip install git+https://github.com/thisgary/descordlib

## Features

`descord/func` - Compilation of functions used in this library.

`descord/bot` - For Discord bot hosting.

`descord/ext` - Discord.py extensions collection.

    from descord import bot, wake
    bot.load('system') # load ext from module
    bot.run(TOKEN) # start bot with token
