# Dscord

Discord API wrapper's wrapper, ironically.

## Purpose

Solely for me to learn how to write a Discord bot

It is no longer actively maintained, since `dscord2` a thing now

## Installation

    pip install git+https://github.com/thisgary/dscord

## Features

`dscord` - Provide minimal setup for Discord bot hosting

`dscord/ext` - Discord.py extensions collection

## Documentation

### `dscord`

Provide minimal setup for Discord bot hosting. ~~(but again, why you need a wrapper for wrapper)~~ This section covers the functions that can be used to kickstart a Discord bot~~, information about the bot's OOTB commands will be covered in later section. But since I am lazy, you would probably never see it~~.

**Example:**

    import dscord
    dscord.load('system')
    dscord.run(TOKEN)

#### `dscord.load(name, package='dscord.ext')`

Load `discord.py` extentions from local modules or packages.

`name`, `package` - Identical to its [original counterpart](https://docs.python.org/3/library/importlib.html#importlib.import_module), `importlib.import_module()`

#### `dscord.run(token)`

Start the Discord bot, identical to `discord.Client().run(token)`.

> Since it is `discord.Client().run(token)` equivalent, any code after this function will obviously, won't be running.

`token` - Access token of Discord bot in *string*.

### `dscord.wake`

Start two threads, one that starts `flask` server and the other one that ping an url every half an hour. Sounds like a weird combo? Well, turned out the url pinger is meant for pinging the flask server started from first thread. It is an ancient technique used for bot hosting on [Replit](https://replit.com) to keep the bot up 24/7.

**Example:**

    import dscord
    import replit
    dscord.wake.up(replit.info.co_url)
    
#### `wake.up(url, debug=False)`

`url` - The hosted replit.co url of an repl, can be obtained by method as shown on example

`debug` - **Optional**. Used to trigger debug mode of pinger, which print out the status code of every requests (ping) on console
