"""
    module for a discord bot that responds to morning greetings
"""
import asyncio
import os

import logging

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand

from dotenv import load_dotenv
import utils

# logs data to the discord.log file,
#  if this file doesn't exist at runtime
#  it is created automatically
from cogs.utilities import Utilities

logger = logging.getLogger('discord')
# logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
logger.setLevel(logging.INFO)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# load the private discord token from .env file.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Initialise the Bot object with an accessible help Command object
helpCommand = DefaultHelpCommand()

bot = commands.Bot(
    command_prefix=".",
    help_command=helpCommand
)

# Setup the General cog with the help command
generalCog = Utilities()
bot.add_cog(generalCog)
helpCommand.cog = generalCog


@bot.event
async def on_ready():
    """
    Do something when the bot is ready to use.
    """
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching,
        name="the sunrise")
        )


async def activity_loop():
    """
    Cycles through different bot activities
    """
    await bot.wait_until_ready()
    i = 0
    while not bot.is_closed():
        if i > 1:
            i = 0
        status = ['the kitchen', 'the bathroom']
        await bot.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching,
            name=status[i])
            )
        await asyncio.sleep(4)
        i += 1


@bot.event
async def on_message(message):
    """
    Respond to the message with a corresponding morning greet
    """
    response = utils.get_morning_response(message)
    if response is not None:
        ctx = await bot.get_context(message)

        await ctx.send(response)

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """
    Handle the Error message in a nice way.
    """
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(error)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    elif isinstance(error, commands.errors.CommandNotFound):
        pass
    else:
        await ctx.send('You are missing a required argument.')
        logging.error(error)


# Start the bot
bot.run(TOKEN)
