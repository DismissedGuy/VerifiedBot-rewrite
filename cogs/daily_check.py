from discord.ext import commands
import discord
import asyncio
import datetime
import config
import utils.misc

async def daily_check(bot):
    await bot.wait_until_ready()
    while not bot.is_closed():
        # wait until midnight (UTC)
        now = datetime.datetime.utcnow()
        sleep_until = datetime.datetime(year=now.year, month=now.month, day=now.day + 1)
        to_sleep = (sleep_until - now).seconds

        await asyncio.sleep(to_sleep)

        # calculate which people to add/remove
        guild = bot.get_guild(config.server_id)
        role = utils.misc.get_role(guild)
        if not guild.get_member(bot.user.id).guild_permissions.manage_roles:
            print('ERROR: No permissions to manage roles. Aborting daily check.')
            continue

        currently_active = [m.id for m in role.members]
        to_add = [m for m in guild.members if
            bot.msgcount.get(m.id, 0) >= config.minimum_messages and m.id not in currently_active]
        to_remove = [m for m in guild.members if
            bot.msgcount.get(m.id, 0) < config.minimum_messages and m.id in currently_active]

        for member in to_add:
            # give role
            try:
                await member.add_roles(role, reason='User has sent {config.minimum_messages}+ messages today.')
                #await member.send('Your status has been updated to _VERIFIED_')
            except discord.Forbidden:
                # can't send DM, but no problem; we'll continue
                pass
            except discord.HTTPException as e:
                # probably a discord problem
                print(f'ERROR: Adding roles to {member} failed with status code {e.status}.')

        for member in to_remove:
            # remove role
            try:
                await member.remove_roles(role, reason='User\'s message amount dropped under {config.minimum_messages}')
                #await member.send('Your status has been updated to _UNVERIFIED_')
            except discord.Forbidden:
                # can't send DM, but no problem; we'll continue
                pass
            except discord.HTTPException as e:
                # probably a discord problem
                print(f'ERROR: Removing roles from {member} failed with status code {e.status}.')

        now = datetime.datetime.utcnow()
        bot.last_check = now
        bot.msgcount = {}

def setup(bot):
    bot.loop.create_task(daily_check(bot))
