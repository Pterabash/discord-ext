import sys
from typing import List

from discord.ext import commands
from blurpold.func import send_embed, subprocess_log, wrap


class System(commands.Cog):
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
            ctx.channel.id, wrap(log, code='bash'), title='Output',
            footer={'text': f'Time taken: {t}s'}
        )


def setup(bot):
    bot.add_cog(System())
