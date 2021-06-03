import discord, os

client = discord.Client()

@client.event
async def on_ready():
	me = discord.Guild.get_member(394771663155101727)
	await me.send('Test')
	exit()

client.run(os.environ['TOKEN'])
