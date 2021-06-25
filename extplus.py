import os
import sys
import sqlite3
from discord.ext import commands
from urllib.request import urlretrieve

create = 'CREATE TABLE IF NOT EXISTS link (url PRIMARY KEY)'
read = 'SELECT url FROM link'
write = 'INSERT OR IGNORE INTO link VALUES(?)'
remove = 'DELETE FROM link WHERE url=?'

bot = commands.Bot(',')


class Ext:
	def __init__(self, url):
		if 'https://' not in url:
			self.url = 'https://raw.githubusercontent.com/' + url
		else:
			self.url = url
		self.file = url.split('/')[-1]
		self.ext = self.file.split('.')[0]

	def load(self):
		urlretrieve(self.url, self.file)
		try:
			bot.load_extension(self.ext)
		except commands.ExtensionAlreadyLoaded:
			bot.reload_extension(self.ext)
		finally:
			os.remove(self.file)

	def unload(self):
		bot.unload_extension(self.ext)


def dbExec(self, sql, url=None):
	with sqlite3.connect('ext.db') as con:
		data = con.execute(sql, (url,))
		rows = [rows[0] for rows in data]
		con.commit()
		con.close()
	return rows

def loadAll():
	for url in dbExec(read):
		Ext(url).load()

class Extension(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(brief='List loaded extensions')
	async def exts(self, ctx):
		for url in dbExec(read):
			msg = '```\n' + url + '```'
			await ctx.send(msg)

	@commands.command(brief='Load extension from internet')
	async def load(self, ctx, url):
		Ext(url).load()
		dbExec(write, url)

	@commands.command(brief='Unload extension')
	async def unload(self, ctx, url):
		Ext(url).unload()
		dbExec(remove, url)

	@commands.command(brief='Reload all extensions')
	async def reload(self, ctx):
		loadAll()


@bot.event
async def on_ready():
	dbExec(create)
	loadAll()

@bot.command(brief='Restart the bot')
async def restart(ctx):
	await ctx.send('Restarting')
	os.execl(sys.executable, sys.executable, *sys.argv)

bot.add_cog(Extension(bot))
bot.run(os.environ['TOKEN'])
