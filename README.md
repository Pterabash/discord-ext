# Discord Ext

Discord.py bot extension examples... Ok, ran out of idea about what to say.

# How to use

Load the extensions file while running a Discord bot.

## Quick hacks

To prevent having to restart bot everytime trying to load extension, one could do something like:

	@bot.commands()
	async def load(ctx, ext):
		bot.load_extension(ext)

Also, feel free to checkout [this thing](https://github.com/cicadoves/discord-cicada)
