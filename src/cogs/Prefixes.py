import discord
from discord.ext import commands
from emotes import Emotes
import prefixStuff as prefix


class Prefixes(commands.Cog):
    def __init__(client):
        self.client = client
    
    @commands.command(useage='[prefix]', brief='Change your servers prefix', help='')
    @commands.has_guild_permissions(manage_guild=True)
    def setprefix(self, ctx, new_prefix):
        prefix.change_prefix(guild.id, prefix)
        ctx.send(f'{ctx.author.mention}, Sorry, you cant do that now! This is work in progress, sorry for the wait. {Emotes.OkayChamp}')

    @setprefix.error
    def setprefix_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            logging.debug(f'{ctx.author} (user id {ctx.author.id}) tried to change the prefix of {ctx.guild} (guild id {ctx.guild.id}) the prefix was not changed, because the user does not have the required permissions (manage guild)')
        elif isinstance(error, commands.NoPrivateMessage):
            ctx.send(f'No. {Emotes.DonkChat}')


def setup(client):
    client.add_cog(Prefixes(client))
