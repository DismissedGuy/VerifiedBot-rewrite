import discord
from discord.ext import commands
import os
import logging
import datetime
import traceback
import config
import utils.msgcount

now = datetime.datetime.utcnow()

logging.basicConfig(level=logging.INFO)

extensions = ['cogs.' + ext.rstrip('.py') for ext in os.listdir('cogs/') if os.path.isfile(f'cogs/{ext}')]

async def get_prefix(bot, message):
    prefixes = ['v!', 'V!']
    return commands.when_mentioned_or(*prefixes)(bot, message)

bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, activity=discord.Game('Say v!help'))
bot.remove_command('help')
bot.startup_time = now
bot.msgcount = utils.msgcount.get()
bot.last_check = now

if __name__ == '__main__':
    for ext in extensions:
        try:
            bot.load_extension(ext)
        except Exception as e:
            print(f'Failed to load extension {ext}.')
            traceback.print_exc()

@bot.event
async def on_ready():
    active_guild = bot.get_guild(config.server_id)
    print(discord.__version__)
    print('-----------')
    print(f'Logged into {bot.user.name} (ID: {bot.user.id})')
    print(f'Serving {active_guild.name}, with {active_guild.member_count} members.')
    print(f'{len(bot.commands)} commands registered.')
    print('-----------')

bot.run(config.token)
