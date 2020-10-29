import asyncio
import os

import logging

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand

from dotenv import load_dotenv
from datetime import datetime
import random
import utils

# logs data to the discord.log file, if this file doesn't exist at runtime it is created automatically
from cogs.utilities import Utilities

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)  # logging levels: NOTSET (all), DEBUG (bot interactions), INFO (bot connected etc)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the sunrise"))


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
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status[i]))
        await asyncio.sleep(4)
        i += 1


async def morning_in():
    """
    Prints a random location of a list where it is currently 8am in their timezone 
    """
    random_location = random.randint(0, 2)

    random_morning = 7 + random.randint(0, 2)

    now = datetime.now()
    now = now.replace(minute=0, second=0, microsecond=0)
    morning = now.replace(hour=random_morning)

    print(now, ' | ', morning)
    
    timezone = utils.calculate_timezone(now,morning)
    
    location = utils.get_location(timezone,random_location)

    return location


@bot.event
async def on_message(message):
    if not message.author.bot and message.content.lower().__contains__("morn"):

        location = await morning_in()

        ctx = await bot.get_context(message)
        await ctx.send(message.author.mention + ' Good morning from ' + location)

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    """<<<<<<< HEAD

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