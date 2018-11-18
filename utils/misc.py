import discord
import config

def get_role(guild):
    role = discord.utils.get(guild.roles, name=config.role_name)
    if not role:
        raise ValueError('No such role with name {config.role_name} found.')
    return role
