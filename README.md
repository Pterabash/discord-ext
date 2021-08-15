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

`dscord/wake` - Used in bot hosting on [Replit](https://replit.com)

# Documentation

This section contain informations about functions that are available on this module. 
~~Information about the bot's OOTB commands will be covered in the next segment, but I am lazy.~~

## `dscord` module

Provide minimal setup for Discord bot hosting.
~~(but again, why you need a wrapper for wrapper)~~ 

    import dscord
    dscord.load('system')
    dscord.run(TOKEN)

### `dscord.load(name, package='dscord.ext')`

Load `discord.py` extentions from local modules or packages.

`name`, `package` - Identical to its [original counterpart](https://docs.python.org/3/library/importlib.html#importlib.import_module), `importlib.import_module()`

### `dscord.run(token)`

Start the Discord bot, identical to `discord.Client().run(token)`.

> Use this on last line of the script

`token` - Access token of Discord bot in *string*.

## `dscord/wake` module

Used in bot hosting on [Replit](https://replit.com) to keep the bot up 24/7. self-pinger included, and **debug mode** returns status code on request.

    from dscord import wake
    import replit
    wake.up(replit.info.co_url)

> It's recommended that one should get some external pingers too
    
### `wake.up(url, debug=False)`

`url` - The hosted replit.co url of an repl, can be obtained by method as shown on example

`debug` - **Optional**. Used to activate **debug mode**.
