"""
    module for a discord bot that responds to morning greetings
"""
import logging
import os

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
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# load the private discord token from .env file.
load_dotenv()

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
async def on_ready() -> None:
    """
    Do something when the bot is ready to use.
    """
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="the sunrise"
        )
    )


@bot.event
async def on_message(message) -> None:
    """
    Respond to the message with a corresponding morning greet
    """
    response = utils.get_morning_response(message)
    if response is not None: await message.channel.send(response)
    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error) -> None:
    """
    Handle the Error message in a nice way.
    """
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(error)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('You are missing a required argument.')
    else:
        await ctx.send('You are missing a required argument.')
        logging.error(error)


def main() -> None: bot.run(os.getenv('DISCORD_TOKEN'))


if __name__ == '__main__':
    main()
