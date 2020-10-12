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
import logging
import check
from emotes import Emotes

# logging configuration
logging.basicConfig(format='[%(asctime)s] (%(name)s) %(levelname)s : %(message)s', 
                    datefmt='%m/%d/%Y %z %H:%M:%S', level=logging.DEBUG)

# load token from .env file
load_dotenv()
CAST_TOKEN = os.getenv('CAST_TOKEN')

# bot start
prefix = 'c.'
client = commands.Bot(command_prefix=prefix)
logging.info(f'Bot prefix is \'{prefix}\'')


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
        cogs = f.read().split('\n')
    cogs_added = str()
    for cog in cogs:
        if cog != '':
            client.load_extension(f'cogs.{cog}')
            cog += ', '
            cogs_added += cog
    logging.info(f'Cogs loaded from startup: {cogs_added[:-2]}')


@client.event
async def on_ready():
    client.add_cog(ExtensionManagement(client))
    load_starting_cogs(client)
    logging.info(f'CAST is ready to battle...')
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('with cute kittens!'))


# cog to manage extensions, cannot be unloaded
class ExtensionManagement(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.check(check.is_admin)
    @commands.command(brief='Load an extension', useage='(extension)', help='Loads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def load(self, ctx, extension):
        if extension not in list(client.cogs):
            client.load_extension(f'cogs.{extension}')
            logging.debug(f'Extension loaded: (triggered by {ctx.author}, id={ctx.author.id})\n{extension}')
            await ctx.send(f'{ctx.author.mention}, {extension} loaded! {Emotes.OkayChamp}')
        else:
            raise commands.ExtensionAlreadyLoaded

    @commands.check(check.is_admin)
    @commands.command(brief='Unload an extension', useage='(extension)', help='Unloads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def unload(self, ctx, extension):
        if extension in list(client.cogs):
            client.unload_extension(f'cogs.{extension}')
            logging.debug(f'Extension unloaded: (triggered by {ctx.author}, id={ctx.author.id})\n{extension}')
            await ctx.send(f'{ctx.author.mention}, {extension} unloaded! {Emotes.OkayChamp}')
        else:
            await ctx.send(f'{ctx.author.mention}, Extension is not loaded! {Emotes.Sadge} Extension has not been unloaded!')

    @commands.check(check.is_admin)
    @commands.command(brief='Reload an extension', useage='(extension)', help='Reloads an extension\n'
    '(extension) must have no spaces and must be a valid extension')
    async def reload(self, ctx, extension):
        if extension in list(self.client.cogs):
            client.reload_extension(f'cogs.{extension}')
            logging.debug(f'Extension loaded: (triggered by {ctx.author}, id={ctx.author.id})\n{extension}')
            await ctx.send(f'{ctx.author.mention}, `{extension}` reloaded! {Emotes.OkayChamp}')
        else:
            await ctx.send(f'{ctx.author.mention}, `{extension}` not loaded! Use `{self.client.command_prefix}load` to load an extension. {Emotes.OkayChamp}')

    @commands.check(check.is_admin)
    @commands.command(brief='Add/remove an extension from startup', 
    aliases=['setup'], 
    usage='[[add|a]|[remove|r]|list|listall] (extension)', 
    help='Adds or removes an extension from startup. If an extension is on startup the next time '
    'the bot starts the extension will be loaded automatically\n'
    '    \'list\' lists all of the extensions in startup\n'
    '    \'listall\' lists all extensions\n'
    '    \'add\' and \'a\' add (extension) to startup\n'
    '    \'remove\' and \'r\' removes (extension) from startup\n'
    '(extension) must have no spaces and must be a valid extension (not needed on \'list\' or \'listall\')\n'
    f'Giving no [action] or (extention) will return the same as \'{client.command_prefix}startup list\'')
    async def startup(self, ctx, action='1 2 3 4 Not An Action 9ef5a42av6483fav95498ab21f948cf649b874cb6tq9wi6b92dcb6t9i73idwt', extension=None):
        newline = '\n'  # I have to do this because `func(f'{'\n'}')` makes it think there is a line continuation character
        if action.lower() in ('a', 'add'):  # adding an extension
            if not extension:
                await ctx.send(f'{ctx.author.mention}, Please provide an extension to add! {Emotes.OkayChamp}')
                return
            if extension in get_all_extensions():
                with open('./src/cogs/on_startup.txt', 'r') as f:
                    if extension in f.read().split('\n'):
                        await ctx.send(f'{ctx.author.mention}, Extension already in startup! Extension not added. {Emotes.OkayChamp}')
                        return
                with open('./src/cogs/on_startup.txt', 'a') as f:
                    f.write(f'{extension}\n')
                await ctx.send(f'{ctx.author.mention}, Extension `{extension}` added to startup. {Emotes.OkayChamp}')
            else:
                await ctx.send(f'{ctx.author.mention}, Extension doesnt exist! Not added to startup. {Emotes.OkayChamp}')
        elif action.lower() in ('r', 'remove'):  # removing an extension
            if not extension:
                await ctx.send(f'{ctx.author.mention}, Please provide an extension to remove! {Emotes.OkayChamp}')
                return
            with open('./src/cogs/on_startup.txt', 'r') as f:
                data = f.read().split('\n')
            if extension not in data:
                await ctx.send(f'{ctx.author.mention}, Extension not in startup! Extension not removed. {Emotes.OkayChamp}')
            for line in data:
                if line == extension:
                    del data[data.index(line)]
            with open('./src/cogs/on_startup.txt', 'w') as f:
                f.write('\n'.join(data))
            await ctx.send(f'{ctx.author.mention}, Extension `{extension}` removed from startup. {Emotes.OkayChamp}')
        elif action.lower() == 'listall':  # list all extensions
            await ctx.send(f'{ctx.author.mention}, Here is all availible extensions:\n```\n{newline.join(get_all_extensions())}```')
        elif action.lower() == 'list' or action == '1 2 3 4 Not An Action 9ef5a42av6483fav95498ab21f948cf649b874cb6tq9wi6b92dcb6t9i73idwt':  # list enabled extensions
            with open('./src/cogs/on_startup.txt', 'r') as f:
                cogs_on_startup = f.read().split('\n')
            await ctx.send(f'{ctx.author.mention}, Here is all extensions on startup: {Emotes.OkayChamp}\n```\n{newline.join(cogs_on_startup)}```')
        else:
            await ctx.send(f'{ctx.author.mention}, Invalid syntax, see `{self.client.command_prefix}help startup` for more information {Emotes.OkayChamp}')

    @unload.error
    @load.error
    async def load_command_error(self, ctx, error):
        # error 1
        if isinstance(error, commands.ExtensionNotFound) or isinstance(error, ModuleNotFoundError):
            logging.debug(f'Error handled from {self.client.command_prefix}{ctx.command.name} (error 1): {error}')
            await ctx.send(f'{ctx.author.mention}, Extension not found! {Emotes.DonkChat}')
        # error 2
        elif isinstance(error, commands.ExtensionNotLoaded):
            logging.debug(f'Error handled from {self.client.command_prefix}{ctx.command.name} (error 2): {error}')
            await ctx.send(f'{ctx.author.mention}, Extension not loaded! {Emotes.DonkChat}')
        # error 3
        elif isinstance(error, commands.MissingRequiredArgument):
            logging.debug(f'Error handled from {self.client.command_prefix}{ctx.command.name} (error 3): {error}')
            await ctx.send(f'{ctx.author.mention}, Please provide an extention to load/unload. {Emotes.DonkChat}')
        # error 4
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            logging.debug(f'Error handled from {self.client.command_prefix}{ctx.command.name} (error 4): {error}')
            await ctx.send(f'{ctx.author.mention}, Extension already loaded! {Emotes.DonkChat} To reload use `{self.client.command_prefix}reload (extension)`')
        # error 5
        elif isinstance(error, SyntaxError):
            logging.debug(f'Error handled from {self.client.command_prefix}{ctx.command.name} (error 5): {error}')
            await ctx.send(f'{ctx.author.mention}, Syntax Error! Check console for more information {Emotes.DonkChat}')
        else:
            logging.error(f'Error in command \'{ctx.command.name}\': \n{error}')


    @reload.error
    async def reload_command_error(self, ctx, error):
        # error 1
        if isinstance(error, commands.ExtensionNotFound) or isinstance(error, ModuleNotFoundError):
            logging.debug(f'Error handled from {self.client.command_prefix}reload (error 1): {error}')
            await ctx.send(f'{ctx.author.mention}, Extension not found! Change Reverted. {Emotes.DonkChat}')
        # error 2
        elif isinstance(error, commands.ExtensionNotLoaded):
            logging.debug(f'Error handled from {self.client.command_prefix}reload (error 2): {error}')
            await ctx.send(f'{ctx.author.mention}, Extension not loaded! Change Reverted. {Emotes.DonkChat}')
        # error 3
        elif isinstance(error, commands.MissingRequiredArgument):
            logging.debug(f'Error handled from {self.client.command_prefix}reload (error 3): {error}')
            await ctx.send(f'{ctx.author.mention}, Please provide an extention to reload. {Emotes.DonkChat}')
        else:
            logging.error('Error in command \'reload\': "%s"', error)


# start the bot
logging.info('Gathering battle gear...')
client.run(CAST_TOKEN)
