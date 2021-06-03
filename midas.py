import discord, os

client = discord.Client()

@client.event
async def on_ready():
	me = discord.Guild.get_member(394771663155101727)
	await me.send('Test')
	await client.logout()

await client.login(os.environ['TOKEN'])
