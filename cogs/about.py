import discord
from discord.ext import commands
import datetime
import psutil
import os
import utils.logs
import config

class About():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def about(self, ctx):
        log_info = utils.logs.get_log_info()
        process = psutil.Process(os.getpid())
        uptime = str(datetime.datetime.utcnow() - self.bot.startup_time).split('.')[0]
        message_amount = sum(self.bot.msgcount.values())
        if message_amount == 0:
            message_amount = 1

        embed = discord.Embed(color=discord.Color.green(), title='About me', description=f"""
:wave: Hi there!
I'm a bot created by <@311869975579066371> (ID: 311869975579066371). My purpose is to keep track of all of your messages so you can get a special role by being active on **{self.bot.get_guild(config.server_id).name}** ^^.
You probably don't see me often; that's because I do almost everything in the background, so next to no user interface is present.
You can check how many messages you've sent by doing **{ctx.prefix}check**. For other commands that may be useful to you, please take a look at **{ctx.prefix}help**.
        """)
        embed.add_field(name='Bot stats', value=f"""
:white_small_square: Uptime: **{uptime}**
:white_small_square: Memory usage: **{round(process.memory_info().rss / 1024 / 1024)}MB ({round(process.memory_percent() * 100) / 100}%)**
:white_small_square: Amount of log files: **{log_info.amount}**
:white_small_square: Size of log directory: **{log_info.size}Kb ({utils.logs.get_logname()})**
        """)
        embed.add_field(name='Message stats', value=f"""
:white_small_square: Recorded messages for today: **{message_amount}**
:white_small_square: Amount of unique members seen today: **{len(self.bot.msgcount)}**
:white_small_square: Percentage of members that were seen today: **{round(len(self.bot.msgcount) / ctx.guild.member_count * 100)}%**
        """)
        await ctx.send(embed=embed)

    @commands.command(aliases=['pung', 'pang', 'pong', 'peng'])
    async def ping(self, ctx):
        """Simple ping command"""
        msg = await ctx.send(f':ping_pong: Pong! Latency: {round(self.bot.latency * 1000)}')
        delay = round((datetime.datetime.utcnow() - msg.created_at).microseconds) // 1000
        await msg.edit(content=f'{msg.content}ms | Message edit: {delay}ms')

    @commands.command()
    async def help(self, ctx, command=None):
        """provides command help"""
        if command:
            #provide help for specified command
            return

        embed = discord.Embed(title='help')
        for name, cog in self.bot.cogs.items():
            cmds = [f':white_small_square: **{command.name}** - {command.help}'
                for command in cog.commands]
            help_str = ':white_small_square: ' + '\n'.join(cmds)
            embed.add_field(name=name, value=help_str)
        await ctx.send(':question: What can I help you with today?', embed=embed)

def setup(bot):
    bot.add_cog(About(bot))
