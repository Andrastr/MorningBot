# https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes

import asyncio
import os

import logging

import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
import random

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


places = [['Cockermouth', 'Höfn í Hornafirði', '(تجكجة (Tidjikja)'],  # 0
         ['Sveargruva', 'Useldange', 'Musadi'], ['Kitwe', 'Пиків Vinnytsia (Pykiv)', 'Pudasjärvi'],  # 1, 2
         ['ጫንጮ (Debre Selam)', 'قيصومة فيحان', 'Ooo "Kara-Tau"'], ['Volgrograd Oblast', 'Crozet Islands', 'Shushi'],  # 3, 4
         ['Mawson Station', 'Gan', 'Margilan'], ['Omsk Oblast', 'Rangpur', 'Oskemen'],  # 5, 6
         ['Khakassia', 'Christmas Island', 'Đà Lạt'], ['Buryatia', 'Changhua', 'Paraburdoo'],  # 7, 8
         ['Zabaykalsky Krai', '熊牛 (Kumaushi)', 'Choll'], ['Kanduka', 'Suicide Cliff', 'Carmila'],  # 9, 10
         ['Loloho', 'Ball Bay Reserve', 'Bopope'], ['Tofia', 'Millers Flat', 'Kanton Island'],  # 11, 12
         ['Howland Island', 'Baker Island', 'The International Date Line'], ['Niue', 'Swains Island', 'Fakofo'],  # -12, -11
         ['Îles du Désappointement', 'Te Ulu-o-Te-Watu', 'Kaua\'i'], ['Knik-Fairview', 'Kwethluk', 'Pleasant Valley'],  # -10, -9
         ['Coeur d\'Alene', 'Catavina', 'Kamloops'], ['Kugluktuk', 'Meeteetse', 'Jordan Valley'],  # -8, -7
         ['Arkabutla Lake', 'Espíritu Santo', 'Saskatchewan'], ['La Havana', 'Sweeting Cay', 'Nippes'],  # -6, -5
         ['Zapallar', 'Nunatsuak', 'Pituffik'], ['Pichi Huinca', 'The Amazon Rainforest', 'Kangerlussuaq'],  # -4, -3
         ['Fernando de Noronha', 'The South Sandwhich Islands', 'Ilha da Trindade'], ['Santa Antão', 'Boa Vista', 'Ittoqqortoormiit']]  # -2, -1



@bot.event
async def on_ready():
    """
    Do something when the bot is ready to use.
    """
    print(f'{bot.user.name} has connected to Discord!')
    # london = pytz.timezone('UTC')
    # pacific = pytz.timezone('Pacific/Honolulu')
    # print(pacific.zone)
    # bla = datetime.now()
    # print(bla)
    # print(pacific)

    # print(pytz.country_names['nz'], pytz.country_timezones['nz'])
    # print(pytz.common_timezones)

    # await bot.loop.create_task(activity_loop())
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
    timezone = 0
    random_location = random.randint(0, 2)
    location = 'Ittoqqortoormiit'
    now = datetime.now()
    now = now.replace(minute=0, second=0, microsecond=0)
    # now = now.replace(hour=22)
    morning = now.replace(hour=8)
    print(now, ' | ', morning)

    if now < morning:
        while now != morning:
            now = now + timedelta(hours=1)
            timezone += 1
        print(timezone)

    elif now > morning:
        while now != morning:
            now = now - timedelta(hours=1)
            timezone -= 1
        print(timezone)

    location = places[timezone][random_location]

    return location

@bot.event
async def on_message(message):
    if message.author.id != 767758780208906241 \
            and message.author.id != 766690857788768289 \
            and message.content.lower().__contains__("morn"):

        location = await morning_in()

        ctx = await bot.get_context(message)
        await ctx.send(message.author.mention + ' Good morning from ' + location)

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
