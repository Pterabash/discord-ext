# Modules

This section contain informations about functions that are available on this module.
~~Information about the bot's OOTB commands will be covered in the next segment, but I am lazy.~~

## `dscord`

Provide minimal setup for Discord bot hosting.
~~(but again, why you need a wrapper for a wrapper)~~

    import dscord
    dscord.load('system')
    dscord.run(TOKEN)

### `dscord.load(name: str, package='dscord.ext': str) -> None`

Load Discord.py extentions from local modules or packages.

`name`, `package` - refer to their [original counterpart](https://docs.python.org/3/library/importlib.html#importlib.import_module).

### `dscord.run(token: str) -> None`

[`run()`](https://discordpy.readthedocs.io/en/stable/api.html#discord.Client.run) equivalent.

`token` - Discord bot's access token.

## `dscord.wake`

Used in bot hosting on [Replit](https://replit.com) to keep the bot up 24/7.
Has an url pinger with **debug mode** that logs ping's status code on console.

    from dscord import wake
    import replit
    wake.up(replit.info.co_url)

> It is still recommended to have some external pingers.

#### `wake.up() -> None`

Start a thread that runs a Flask server and another thread that self ping every 5 minutes.
