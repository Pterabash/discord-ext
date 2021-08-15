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

## Quick Reference

### dscord

#### dscord.**load(name, package)**

`name`, `package` - refer to their [original counterpart](https://docs.python.org/3/library/importlib.html#importlib.import_module)

#### dscord.**run(token)**

`token` - **String**, Discord bot's access token

### dscord/wake

#### wake.**up(url, debug=False)**

`url` - **String**, target url to be pinged every half hour

`debug` - **Optional boolean**, used to activate **debug mode**


## Modules

This section contain informations about functions that are available on this module. 
~~Information about the bot's OOTB commands will be covered in the next segment, but I am lazy.~~

### dscord

Provide minimal setup for Discord bot hosting.
~~(but again, why you need a wrapper for wrapper)~~ 

    import dscord
    dscord.load('system')
    dscord.run(TOKEN)

#### `dscord.load(name, package='dscord.ext')`

Load Discord.py extentions from local modules or packages.

#### `dscord.run(token)`

Start the Discord bot, identical to `discord.Client().run(token)`.

### dscord/wake

Used in bot hosting on [Replit](https://replit.com) to keep the bot up 24/7. 
Has an url pinger with **debug mode** that logs ping's status code on console.

    from dscord import wake
    import replit
    wake.up(replit.info.co_url)

> It is still recommended to have some external pingers

#### `wake.up(url, debug=False)`

Start a thread that runs a Flask server and start another thread that does GET request (act as ping) from url every half an hour.
