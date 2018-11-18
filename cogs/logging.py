import discord
from discord.ext import commands
import datetime
import asyncio
import json
import utils.msgcount
import config

class Logging():
    """Keeps track of people's messages and writes the amounts to a log file"""
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.update_logs())

    async def on_message(self, message):
        """Keeps track of message counts"""
        if message.author.bot:
            return

        if not message.guild or '{-nolog}' in message.channel.topic or message.channel.id in config.ignored_channels:
            #ignore this channel/DM
            return

        context = await self.bot.get_context(message)
        if context.command:
            #command invoked, don't count
            return

        author_id = message.author.id
        current_count = self.bot.msgcount.get(author_id, 0)
        self.bot.msgcount[author_id] = current_count + 1

    async def update_logs(self):
        """updates the appropriate message log"""
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            utils.msgcount.dump(self.bot.msgcount)
            await asyncio.sleep(config.logging_interval)

def setup(bot):
    bot.add_cog(Logging(bot))
