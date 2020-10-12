import discord
from discord.ext import commands
import check
import logging


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.check(check.is_admin)
    @commands.command(brief='Responds with your message', useage='{words}',
    help='Responds with your message, if it can, it will use the emotes too.')
    async def echo(self, ctx, *, words):
        await ctx.send(f'{words}')
        
    @commands.check(check.is_admin)
    @commands.command(brief='List all extensions loaded', help='List all loaded extensions.',
    aliases=['loaded'])
    async def extensions(self, ctx):
        newline = '\n'
        await ctx.send(f'{ctx.author.mention}, Here are all the loaded extensions: <:OkayChamp:762179359993757707>\n```\n{newline.join(list(self.client.cogs))}```')

    @commands.check(check.is_admin)
    @commands.command(aliases=['print'], brief='Print text to the console', useage='{' + 'words}', 
    help='Prints what you tell it to, to the console.\n'
    'For example, useful for getting the text needed to send an emote')
    async def p(self, ctx, *, words=None):
        if words == None:
            words = ''
        logging.info(f'Printing to console via {self.client.command_prefix}p: (triggered by {ctx.author}, id={ctx.author.id}) : `{words}`')
        await ctx.send(f'{ctx.author.mention}, Printed to console! <:OkayChamp:762179359993757707>')


def setup(client):
    client.add_cog(Admin(client))