import main
import sqlite3
import discord
from discord.ext import commands

def wl_exec(sql, *val):
	con = sqlite3.connect('wl.db')
	con.execute(sql,tuple(val))
	con.commit()
	con.close()

sql = 'CREATE TABLE IF NOT EXISTS whitelist (id INTEGER PRIMARY KEY)'
wl_exec(sql)

#@bot.check
#async def check(ctx):
#    author_id = str(ctx.author.id)
#    try: 
#        whitelist = open('whitelist').read()
#        return author_id in whitelist
#    except: 
#        open('whitelist', 'w').write(author_id)
#        return True

@commands.command('wl', brief="List whitelisted members' ID")
async def wl_list(self, ctx, member:discord.Member):
	con = sqlite3.connect('wl.db')
	sql = 'SELECT id FROM whitelist'
	data = con.execute(sql)
	urls = [rows[0] for rows in data]
	con.close()
	await ctx.send('\n'.join(urls))

@commands.command('add', brief='Add member to whitelist')
async def wl_add(self, ctx, member:discord.Member):
	sql = 'INSERT OR IGNORE INTO whitelist VALUES(?)'
	wl_exec(sql, member.id)

@commands.command('rmv', brief='Remove member from whitelist')
async def wl_rmv(self, ctx, member:discord.Member):
	sql = 'DELETE FROM whitelist WHERE id=?'
	if ctx.author.id not member.id: wl_exec(sql, member.id)
	else: await ctx.send('Why remove yourself?')

def setup(bot):
	bot.add_cog(Whitelist(bot))
