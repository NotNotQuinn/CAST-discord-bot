import discord
from discord.ext import commands
import check
from emotes import Emotes

class BasicCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{ctx.author.mention}, Pong! {round(self.client.latency * 1000)}ms {Emotes.OkayChamp}')

    @commands.command()
    async def commands(self, ctx):
        await ctx.send(f'{ctx.author.mention}, Use `{self.client.command_prefix}help` for a list of commands you can use. {Emotes.OkayChamp}')

    async def typing(self, ctx):
        async with ctx.typing():
            time.sleep(7)
            await ctx.send(f'{ctx.author.mention}, Sorry for the wait! I\'m done typing now though! {Emotes.OkayChamp}')


def setup(client):
    client.add_cog(BasicCommands(client))