# discord-ext

Discord.py bot extensions

# How to use
For example, you have `ext.py` located at the same directory with `main.py`. You can load the extension file by doing:

	from discord.ext import commands
	bot = commands.Bot(',')
	bot.load_extension(ext)

## Quick hacks

To prevent having to restart the bot everytime just to load an extension, one could do something like:

	@bot.commands()
	async def load(ctx, ext):
		bot.load_extension(ext)

