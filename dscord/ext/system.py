import os
import sys
from typing import List

from discord.ext import commands

from dscord.func import sub_logs


def pip(args: List[str], inp: str = None):
    args = [sys.executable, '-m', 'pip'] + args
    return sub_logs(args, inp)


class System(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        if isinstance(err, commands.CommandNotFound) or isinstance(err, commands.CheckFailure): return
        print(err)
        await ctx.send(err)

    @commands.command('pipinst')
    async def pipInstall(self, ctx, *, package):
        logs = pip(['install', package])
        for log in logs: await ctx.send(log)

    @commands.command('pipunst')
    async def pipUninstall(self, ctx, *, package): 
        logs = pip(['uninstall', package], b'y')
        for log in logs: await ctx.send(log)


def setup(bot):
    bot.add_cog(System())
