import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    async def echo(self, ctx):
        await ctx.send(f'{ctx.author.mention}, Pong! {round(self.client.latency * 1000)}ms')


def setup(client):
    client.add_cog(Admin(client))