# Imports
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from ascii_art import ascii_art
from os import getenv
from random import seed, choice
import logging

# logging configuration
logging.basicConfig(format='[%(asctime)s] (%(name)s) %(levelname)s : %(message)s', 
                    datefmt='%m/%d/%Y %z %H:%M:%S', level=logging.INFO)

# ascii art & credit
seed()
print(choice(ascii_art))
print('Your running CAST by NotQuinn#6953')

# load token from .env file
load_dotenv()
CAST_TOKEN = getenv('CAST_TOKEN')

# remove no longer needed imports
del ascii_art, seed, choice, getenv, load_dotenv

# bot start
client = commands.Bot(command_prefix='c.')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with cute kittens!'))
    print('CAST is ready to battle...')


# cog to manage extentions, cannot be unloaded
class ExtentionManagement(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(brief='Load an extention', useage='[extention]', help='Loads an extention\n'
    '[extention] must have no spaces and must be a valid extention')
    async def load(self, ctx, *, extention=None):
        client.load_extension(f'cogs.{extention}')
        await ctx.send(f'{ctx.author.mention}, {extention} loaded!')

    @commands.command(brief='Unload an extention', useage='[extention]', help='Unloads an extention\n'
    '[extention] must have no spaces and must be a valid extention')
    async def unload(self, ctx, *, extention=None):
        client.unload_extension(f'cogs.{extention}')
        await ctx.send(f'{ctx.author.mention}, {extention} unloaded!')

    @commands.command(brief='Reload an extention', useage='[extention]', help='Reloads an extention\n'
    '[extention] must have no spaces and must be a valid extention')
    async def reload(self, ctx, *, extention=None):
        client.reload_extension(f'cogs.{extention}')
        await ctx.send(f'{ctx.author.mention}, {extention} reloaded!')

    @commands.command(brief='Add/remove an extention from startup', usage='[action] [extention]', 
    help='Adds or removes an extention from startup. If an extention is on startup the next time '
    'the bot starts the extention will be loaded automatically\n'
    '[extention] must have no spaces and must be a valid extention\n'
    '[action] can be one of: \'add\' \'a\' \'remove\' \'r\' or \'list\'')
    async def startup(self, ctx, action=None, *, extention=None):
        if not action or action.lower() not in ('add', 'a', 'remove', 'r', 'list') or extention.find(' ') != -1 or not extention:
            await ctx.send(f'{ctx.author.mention}, Invalid syntax, see `{self.client.command_prefix}help startup` for more information')
        elif action.lower() in ('a', 'add'):
            with open('./cogs/on_startup.txt', 'a') as file:
                file.write(f'\n{extention}')
                await ctx.send(f'{ctx.author.mention}, Extention \'{extention}\' added to startup.')
        elif action.lower() in ('r', 'remove'):
            with open('./cogs/on_startup.txt', 'r') as f:
                data = f.read()
            data = data.split('\n')
            for line in data:
                if line == extention:
                    del line
            with open('./cogs/on_startup.txt', 'w') as f:
                f.write(data.join('\n'))



def load_starting_cogs(client):
    with open('./cogs/on_startup.txt', 'r') as file:
        data = file.read().split('\n')
        startup_cogs = list()
        for line in data:
            startup_cogs.append(str(line))
    
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename in startup_cogs:
            client.load_extension(f'cogs.\'{filename[:-3]}\'')


# add the ExtentionManagement cog and load cogs in ./cogs/on_startup.txt
client.add_cog(ExtentionManagement(client))
load_starting_cogs(client)

# start the bot
print('Gathering battle gear...')
client.run(CAST_TOKEN)
