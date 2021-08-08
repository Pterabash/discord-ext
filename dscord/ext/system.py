from discord.ext import commands

import os, sys
from dscord.func import log_proc


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound): return
        print(err)
        if isinstance(err, commands.CheckFailure): return
        await ctx.send(err)

    @commands.command(
            'restart',
            aliases=['respawn', 'retard'])
    async def sysRestart(self, ctx):
        await ctx.send('Restarting')
        os.execl(sys.executable, sys.executable, *sys.argv)

    @commands.command(
            'pipinst',
            aliases=['pipadd'])
    async def sysPipInstall(self, ctx, package):
        log = log_proc([sys.executable, '-m', 'pip', 'install', package])
        for x in log: await ctx.send(x)

    @commands.command(
            'pipunst',
            aliases=['piprmv'])
    async def sysPipUninstall(self, ctx, package):
        log = log_proc([sys.executable, '-m', 'pip', 'uninstall', package], b'y')
        for x in log: await ctx.send(x)


def setup(bot):
    bot.add_cog(System(bot))

