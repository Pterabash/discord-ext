import os, subprocess
from discord.ext import commands


class code:
    @staticmethod
    def open(ext, code): open(f'code/input.{ext}', 'w').write(code)

    @staticmethod
    def run(*args):
        subprocess.run(args=args,
                stdout=open('code/output.txt', 'w'),
                stderr=subprocess.STDOUT,
                timeout=10)

    @staticmethod
    def log():
        stdout = open('code/ouput.txt').read()
        x = 2000
        return [stdout[y-x:y] for y in range(x, len(stdout)+x, x)]


class Programming(commands.Cog):
    def __init__(self, bot): self.bot = bot
    
    @commands.command(brief='code() run() log() inp path')
    async def add(self, ctx, ext, *args):
        task = '\n	'.join(args)
        code = f'''import subprocess
from ext.programming import code
from discord.ext import commands

@commands.command()
async def {ext}(ctx, *, code):
    ext = '{ext}'
    {task}
    for log in code.log(): await ctx.send(log)

def setup(bot): bot.add_command({ext})'''
        code = code.replace('code.open()', 'code.open(ext, code)')
	open('code/'+ext+'.py', 'w').write(code)
	try: self.bot.unload_extension('code.'+ext)
    	except: pass
	self.bot.load_extension('code.'+ext)


def setup(bot): 
    try: os.mkdir('code')
    except: print('code directory exists')
    bot.add_cog(Programming(bot))
