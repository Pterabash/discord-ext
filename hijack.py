from discord.ext import commands

import os
import io
import sys

bot = commands.Bot('')

@bot.command()
async def shut(ctx):
  await ctx.send('shutdown')
  exit()
  
@bot.command()
async def test(ctx):
  await ctx.send("OBVIOUSLY I'M ALIVE ||DXCK HEAD||! DON'T YOU KNOW HOW TO LOOK AT BOT STATUS")

@bot.command()
async def py(ctx, *, code):
  sys.stdout = output = io.StringIO()
  open('code.py', 'w').write(code)
  exec(open('code.py').read())
  os.remove('code.py')
  out = output.getvalue()
  x, y = 0, len(out)
  while y >= 2000:
    await ctx.send(out[x:x+2000])
    x += 2000
    y -= 2000
  else:
    await ctx.send(out[x:len(out)])

@bot.command()
async def ext(ctx, ext):
  bot.load_extension(ext)

class instance(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, commands.CommandNotFound): return
    await ctx.send(error)

bot.add_cog(instance(bot))

token = ''
bot.run(token)