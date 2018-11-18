import discord
from discord.ext import commands
from datetime import datetime
import utils.misc
import config

class Checking():
    """Commands for users to check their statuses"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['lead'])
    async def leaderboard(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        sorted_messages = sorted(self.bot.msgcount.keys(), key=lambda v: self.bot.msgcount[v], reverse=True)

        author_place = 'You haven\'t sent any messages yet.'
        if member.id in sorted_messages:
            author_place = f'You\'re **#{sorted_messages.index(member.id) + 1}**!'

        emotes = {
        0: ':first_place:',
        1: ':second_place:',
        2: ':third_place:',
        3: ':four:',
        4: ':five:'
        }
        get_user = lambda value: f'**{ctx.guild.get_member(value)}**' if member.id == value else ctx.guild.get_member(value)
        leaderboard = '\n'.join([f'{emotes[index]} - {get_user(value)} - {self.bot.msgcount[value]} messages' for (index, value) in enumerate(sorted_messages[:5])])

        embed = discord.Embed(title='Leaderboard', description=leaderboard if leaderboard else 'Nobody has sent a message yet :cry:', color= discord.Color.green())
        embed.add_field(name='Your spot on the leaderboard', value=author_place, inline=True)
        embed.set_footer(text=f'▫ Tip: do {ctx.prefix}check to get more detailed info about your messages.')
        await ctx.send(f':white_check_mark: Leaderboard for **{member}**:', embed=embed)

    @commands.command()
    async def check(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author

        amount = self.bot.msgcount.get(member.id)
        if not amount:
            amount = 0
        left = config.minimum_messages - amount
        role = utils.misc.get_role(self.bot.get_guild(config.server_id))
        now = datetime.utcnow()

        desc = f':alarm_clock: Observing your messages for **{now - self.bot.last_check}**.'
        if amount == 0:
            desc = ':warning: **You haven\'t sent any messages yet!**' + f'\n{desc}'

        color = discord.Color.green() if amount >= config.minimum_messages else discord.Color.red()

        embed = discord.Embed(description=desc, color=discord.Color.green())
        embed.add_field(name='Message statistics', value=f"""
:white_small_square: Amount of messages you've sent today: **{amount}/{config.minimum_messages}**
:white_small_square: Eligible for verification: **{amount >= config.minimum_messages} ({left if left > 0 else 0} messages left)**
:white_small_square: Currently {role}: **{ctx.author in role.members}**
        """)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(f':white_check_mark: Stats for **{member}**:', embed=embed)


def setup(bot):
    bot.add_cog(Checking(bot))
