import discord
from discord.ext import commands
import asyncio
import io
import traceback
import textwrap
from contextlib import redirect_stdout
from asyncio import subprocess
import os
from utils import *

class Owner():
    """owner commands"""
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        """check if owner for all commands"""
        return await self.bot.is_owner(ctx.author)

    @commands.command(name='eval')
    async def _eval(self, ctx, *, body: str):
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message
        }

        env.update(globals())
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command(aliases=['cmd'])
    async def bash(self, ctx, *, command):
        """Executes terminal commands on the host"""
        p = await subprocess.create_subprocess_shell(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, _ = await p.communicate()
        out = out.decode().strip()

        await ctx.message.add_reaction('\u2705')
        if out:
            await ctx.send(f'```\n{out}\n```')

    @commands.command()
    async def reload(self, ctx):
        """Unloads all extensions and loads them again"""
        extensions = [file.rstrip('.py') for file in os.listdir('cogs/') if os.path.isfile(f'cogs/{file}')]

        res = ''
        for ext in extensions:
            try:
                self.bot.unload_extension(f'cogs.{ext}')
                self.bot.load_extension(f'cogs.{ext}')
                res += f'✅ - {ext}\n'
            except Exception as e:
                res += f'❌ - {ext}\n{e}'
                break
        await ctx.send(f'```\n{res}\n```')

def setup(bot):
    bot.add_cog(Owner(bot))
