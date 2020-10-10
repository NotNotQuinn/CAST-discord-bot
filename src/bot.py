# Imports
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from ascii_art import ascii_art
from os import getenv
import logging

# logging configuration
logging.basicConfig(format='[%(asctime)s] (%(name)s) %(levelname)s : %(message)s', 
                    datefmt='%m/%d/%Y %z %H:%M:%S', level=logging.INFO)

# ascii art & credit
print(' _______ _______ _______ _______\n'
      ' |       |_____| |______    |   \n'
      ' |_____  |     | ______|    |   ')
print('Your running CAST by NotQuinn#6953')

# load token from .env file
load_dotenv()
CAST_TOKEN = getenv('CAST_TOKEN')

# remove no longer needed imports
del ascii_art, getenv, load_dotenv

# bot start
client = commands.Bot(command_prefix='c.')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with cute kittens!'))
    print('CAST is ready to battle...')


# cog to manage extensions, cannot be unloaded
class ExtensionManagement(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(brief='Load an extension', useage='(extension)', help='Loads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def load(self, ctx, extension):
        client.load_extension(f'cogs.{extension}.py')
        await ctx.send(f'{ctx.author.mention}, {extension} loaded!')

    @commands.command(brief='Unload an extension', useage='(extension)', help='Unloads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def unload(self, ctx, extension):
        client.unload_extension(f'cogs.{extension}.py')
        await ctx.send(f'{ctx.author.mention}, {extension} unloaded!')

    @commands.command(brief='Reload an extension', useage='(extension)', help='Reloads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def reload(self, ctx, extension):
        client.reload_extension(f'cogs.{extension}.py')
        await ctx.send(f'{ctx.author.mention}, {extension} reloaded!')

    @commands.command(brief='Add/remove an extension from startup', aliases=['setup'], usage='[[add|a]|[remove|r]|list|listall] (extension)', 
    help='Adds or removes an extension from startup. If an extension is on startup the next time '
    'the bot starts the extension will be loaded automatically\n'
    '    \'list\' lists all of the extensions in startup\n'
    '    \'listall\' lists all extensions\n'
    '    \'add\' and \'a\' add (extension) to startup\n'
    '    \'remove\' and \'r\' removes (extension) from startup\n'
    '(extension) must have no spaces and must be a valid extension (not needed on \'list\' or \'listall\')\n'
    f'Giving no [action] or (extention) will return the same as \'{client.command_prefix}startup list\'')
    async def startup(self, ctx, action, extension=None):
        newline = '\n'  # I have to do this because `func(f'{'\n'}')` makes it think I want to continue the line
        if action.lower() in ('a', 'add') and extension:  # adding an extension
            if not extension:
                await ctx.send(f'{ctx.author.mention}, Please provide an extension to remove!')
                return
            with open('./src/cogs/on_startup.txt', 'a') as file:
                file.write(f'\n{extension}')
                await ctx.send(f'{ctx.author.mention}, Extension `{extension}` added to startup.')
        elif action.lower() in ('r', 'remove'):  # removing an extension
            if not extension:
                await ctx.send(f'{ctx.author.mention}, Please provide an extension to remove!')
                return
            with open('./src/cogs/on_startup.txt', 'r') as f:
                data = f.read()
            data = data.split('\n')
            for line in data:
                if line == extension:
                    del line
            with open('./src/cogs/on_startup.txt', 'w') as f:
                f.write('\n'.join(data))
            await ctx.send(f'{ctx.author.mention}, Extension `{extension}` removed from startup.')
        elif action.lower() == 'listall':  # list all extensions
            filenames = os.listdir('./src/cogs')
            for filename in filenames:
                if filename.endswith('.py'):
                    filenames[filenames.index(filename)] = filename[:-3]
                else:
                    filenames.remove(filename)
            filenames.remove('__pycache__')  # idk, it doesnt remove it in the for loop
            await ctx.send(f'{ctx.author.mention}, Here is all availible extensions:\n```\n{newline.join(filenames)}```')
        elif action.lower() == 'list':  # list enabled extensions
            with open('./src/cogs/on_startup.txt', 'r') as f:
                enabled_extensions = f.readlines()
            await ctx.send(f'{ctx.author.mention}, Here is all enabled extensions:\n```\n{newline.join(enabled_extensions)}```')
        else:
            await ctx.send(f'{ctx.author.mention}, Invalid syntax, see `{self.client.command_prefix}help startup` for more information')

    @startup.error
    async def startup_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, Please provide an action, see `{client.command_prefix}help startup` for more information.')

    @unload.error
    @load.error
    async def load_error(self, ctx, error):
        if isinstance(error, commands.ExtensionNotFound) or isinstance(error, ModuleNotFoundError):
            await ctx.send(f'{ctx.author.mention}, Extension not found!')
        elif isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send(f'{ctx.author.mention}, Extension not loaded!')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, Please provide an extention to load/unload.')

    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.ExtensionNotFound) or isinstance(error, ModuleNotFoundError):
            await ctx.send(f'{ctx.author.mention}, Extension not found! Change Reverted.')
        elif isinstance(error, commands.ExtensionNotLoaded):
            await ctx.send(f'{ctx.author.mention}, Extension not loaded! Change Reverted.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, Please provide an extention to reload.')





def load_starting_cogs(client):
    with open('./src/cogs/on_startup.txt', 'r') as f:
        data = f.read().split('\n')
    startup_cogs = list()
    for line in data:
        startup_cogs.append(line)
    for filename in os.listdir('./src/cogs'):
        if filename.endswith('.py') and filename in startup_cogs:
            client.load_extension(f'cogs.\'{filename[:-3]}\'')


# add the ExtensionManagement cog and load cogs in ./src/cogs/on_startup.txt
client.add_cog(ExtensionManagement(client))
load_starting_cogs(client)

# start the bot
print('Gathering battle gear...')
client.run(CAST_TOKEN)
