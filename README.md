# ext
Discord.py bot extensions

# How to use
Load the extensions file while running a Discord bot.

## Quick hacks
To prevent having to restart the bot for **n** times everytime trying to load an extension, one could do something like:

	@bot.commands()
	async def load(ctx, ext):
		bot.load_extension(ext)

Also, feel free to checkout [this thing](https://github.com/cicadoves/bot)
