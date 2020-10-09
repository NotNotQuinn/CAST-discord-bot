# Imports
import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
from ascii_art import ascii_art
from os import getenv
from random import (
    seed,
    choice)
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

# errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.mention}, ERROR! Please pass in all required arguments. For more information')
    elif isinstance(error, commands.DisabledCommand):
        

# cog to manage extentions, cannot be unloaded
class ExtentionManagement(commands.cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(brief='Load an extention', useage='[extention]')
    async def load(self, ctx, *, extention=None):
        client.load_extension(f'cogs.{extention}')
        await ctx.send(f'{ctx.author.mention}, {extention} loaded!')

    @commands.command(brief='Unload an extention', useage='[extention]')
    async def unload(self, ctx, *, extention=None):
        client.unload_extension(f'cogs.{extention}')
        await ctx.send(f'{ctx.author.mention}, {extention} unloaded!')

    @commands.command(brief='Reload an extention', useage='[extention]')
    async def reload(self, ctx, *, extention=None):
        client.reload_extension(f'cogs.{extention}')
        await ctx.send(f'{ctx.author.mention}, {extention} reloaded!')

    @commands.command(brief='Add/remove an extention from startup', usage='[(add/a)/(remove/r)] [extention]')
    async def startup(self, ctx, action=None, *, extention=None):
        if not action or action.lower() not in ('add', 'a', 'remove', 'r'):
            await ctx.send(f'{ctx.author.mention}, Invalid syntax, see {self.client.command_prefix}help startup for more information')
            return
        

def load_starting_cogs(client):
    with open('./cogs/on_startup.txt', 'r') as file:
        data = file.read().split('\n')
        startup_cogs = list()
        for line in data:
            startup_cogs.append(str(line))
    
    for filename in os.listdir('./cogs'):
        print(filename)
        if filename.endswith('.py') and filename in startup_cogs:
            client.load_extension(f'cogs.\'{filename[:-3]}\'')


# load cogs in on_startup.txt
load_starting_cogs(client=client)

# start the bot
print('Gathering battle gear...')
client.run(CAST_TOKEN)
