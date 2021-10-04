import sys
from typing import List

from discord.ext import commands
from dscord.func import send_embed, subprocess_log, wrap


class System(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, err) -> None:
        if (
            isinstance(err, commands.CommandNotFound) 
            or isinstance(err, commands.CheckFailure)
        ):
            return
        print(err)
        send_embed(
            ctx.channel.id, 
            wrap(str(err), lang='bash'), title='Error'
        )

    @commands.command('pip')
    async def pip(self, ctx, mode, package) -> None:
        if mode == 'i':
            log, t = subprocess_log(['install', package])
        elif mode == 'u':
            log, t = subprocess_log(['uninstall', package], b'y')
        else:
            await ctx.send('`Invalid mode (i or u)`')
            return
        send_embed(
            ctx.channel.id, wrap(log, lang='bash'), title='Output',
            footer={'text': f'Time taken: {t}s'}
        )


def setup(bot):
    bot.add_cog(System())
