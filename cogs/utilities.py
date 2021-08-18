"""
Module for general utilities for discord bot
"""

import time
from discord.ext import commands
from discord.ext.commands import Context


class Utilities(commands.Cog):
    """
    General Utilities
    """

    @commands.command()
    async def ping(self, ctx: Context):
        """
        Status check
        """
        start_time = time.time()
        message = await ctx.send(
            'pong. `DWSP latency: ' +
            str(round(ctx.bot.latency * 1000)) +
            'ms`'
        )
        end_time = time.time()
        await message.edit(
            content='pong. `DWSP latency: ' +
                    str(round(ctx.bot.latency * 1000)) +
                    'ms` ' +
                    '`Response time: ' +
                    str(int((end_time - start_time) * 1000)) +
                    'ms`')

    @commands.command()
    async def source(self, ctx: Context):
        """
        Print a link to the source code
        """
        await ctx.send(
            content='Created by `Andreas` and `Joel`, brought to you by `Joel Adams & co`\n'
                    'Thanks to the contributors:\n'
                    '`Philip`, `Matt`, `Michael`, `Prv`, `Jazzyboy1`\n'
                    'https://github.com/Andrastr/MorningBot')

    @commands.command()
    async def feedback(self, ctx: Context):
        """
        Report feedback or issues with the bot
        """
        await ctx.send(
            'If the bot is broken or you have any feedback '
            'you\'d like to submit please create a issue on:'
            'GitHub: https://github.com/Andrastr/MorningBot')
