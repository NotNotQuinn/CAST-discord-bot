import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def echo(self, ctx, *, words):
        await ctx.send(f'{words}')


def setup(client):
    client.add_cog(Admin(client))