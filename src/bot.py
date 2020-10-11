# ascii art & credit
print(' _______ _______ _______ _______\n'
      ' |       |_____| |______    |   \n'
      ' |_____  |     | ______|    |   ')
print('Your running CAST by NotQuinn#6953')

# Imports
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import logging
import check

# logging configuration
logging.basicConfig(format='[%(asctime)s] (%(name)s) %(levelname)s : %(message)s', 
                    datefmt='%m/%d/%Y %z %H:%M:%S', level=logging.INFO)

# load token from .env file
load_dotenv()
CAST_TOKEN = getenv('CAST_TOKEN')

# remove no longer needed imports
del getenv, load_dotenv

# bot start
prefix = 'c.'
client = commands.Bot(command_prefix=prefix)
logging.info('Bot prefix is \'%s\'', prefix)


def get_all_extensions():
    filenames = os.listdir('./src/cogs')
    for filename in filenames:
        if filename.endswith('.py'):
            filenames[filenames.index(filename)] = filename[:-3]
        else:
            filenames.remove(filename)
    filenames.remove('__pycache__')  # idk, it doesnt remove it in the for loop
    return filenames


def load_starting_cogs(client):
    with open('./src/cogs/on_startup.txt', 'r') as f:
        cogs = f.readlines()
    cogs_added = []
    for cog in cogs:
        client.load_extension(f'cogs.{cog}')
        cog += ', '
        cogs_added.append(cog)
    logging.info(f'Cogs loaded from startup: {cogs_added[:-2]}')


@client.event
async def on_ready():
    client.add_cog(ExtensionManagement(client))
    load_starting_cogs(client)
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with cute kittens!'))
    logging.info('CAST is ready to battle...')


# cog to manage extensions, cannot be unloaded
class ExtensionManagement(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.check(check.is_admin)
    @commands.command(brief='Load an extension', useage='(extension)', help='Loads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def load(self, ctx, extension):
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f'{ctx.author.mention}, {extension} loaded!')

    @commands.check(check.is_admin)
    @commands.command(brief='Unload an extension', useage='(extension)', help='Unloads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def unload(self, ctx, extension):
        client.unload_extension(f'cogs.{extension}')
        await ctx.send(f'{ctx.author.mention}, {extension} unloaded!')

    @commands.check(check.is_admin)
    @commands.command(brief='Reload an extension', useage='(extension)', help='Reloads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def reload(self, ctx, extension):
        client.reload_extension(f'cogs.{extension}')
        await ctx.send(f'{ctx.author.mention}, {extension} reloaded!')

    @commands.check(check.is_admin)
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
            if extension in get_all_extensions():
                with open('./src/cogs/on_startup.txt', 'a') as f:
                    f.write(f'\n{extension}')
                await ctx.send(f'{ctx.author.mention}, Extension `{extension}` added to startup.')
            else:
                await ctx.send(f'{ctx.author.mention}, Extension doesnt exist! Not added to startup.')
        elif action.lower() in ('r', 'remove'):  # removing an extension
            if not extension:
                await ctx.send(f'{ctx.author.mention}, Please provide an extension to remove!')
                return
            with open('./src/cogs/on_startup.txt', 'r') as f:
                data = f.readlines()
            for line in data:
                if line == extension:
                    del data[data.index(line)]
            with open('./src/cogs/on_startup.txt', 'w') as f:
                f.write('\n'.join(data))
            await ctx.send(f'{ctx.author.mention}, Extension `{extension}` removed from startup.')
        elif action.lower() == 'listall':  # list all extensions
            await ctx.send(f'{ctx.author.mention}, Here is all availible extensions:\n```\n{newline.join(get_all_extensions())}```')
        elif action.lower() == 'list':  # list enabled extensions
            with open('./src/cogs/on_startup.txt', 'r') as f:
                cogs_on_startup = f.readlines()
            await ctx.send(f'{ctx.author.mention}, Here is all extensions on startup:\n```\n{newline.join(cogs_on_startup)}```')
        else:
            await ctx.send(f'{ctx.author.mention}, Invalid syntax, see `{self.client.command_prefix}help startup` for more information')

    @startup.error
    async def startup_command_error(self, ctx, error):
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


# start the bot
logging.info('Gathering battle gear...')
client.run(CAST_TOKEN)
