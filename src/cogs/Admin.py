import discord
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def echo(self, ctx, *, words):
        await ctx.send(f'{words}')

    @commands.command()
    async def extensions(self, ctx):
        await ctx.send(f'{ctx.author.mention}, Here are all the loaded extensions:\n```\n{self.client.cogs}```')        


def setup(client):
    client.add_cog(Admin(client))