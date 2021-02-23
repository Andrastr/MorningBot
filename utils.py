"""
Module for core functionality of morningbot
"""
from datetime import timedelta
from datetime import datetime
import enum
import json
import random

class TriggerStatus(enum.Enum):
    Regular = 0
    Reverse = 1

# Define list of morning response triggering substrings
morningTriggers = {
    "morning": "{user} Good morning from {place}",
    # Brythonic
    "bore": "{user} Bore da o {place}",
    "myttin": "{user} Myttin da diworth {place}",
    "demat": "{user} Mintinvezh mat eus {place}",
    "mintin": "{user} Mintinvezh mat eus {place}",
    "beure": "{user} Beurevezh mat eus {place}",
    # Gaelic / Goidelic
    "madainn mhath": "{user} Madainn mhath bho {place}",
    "maidin mhaith": "{user} Maidin mhaith ó {place}",
    "moghrey mie": "{user} Moghrey mie voish {place}",
    # Germanic
    "guten morgen": "{user} Guten morgen ab {place}",
    "góðan daginn": "{user} Góðan daginn frá {place}",
    "god morgen": "{user} God morgen fra {place}",
    "god morgon": "{user} God morgon frå {place}",
    # Latin
    "bon matin": "{user} Bonjour de {place}",
    "bonjour": "{user} Bonjour de {place}",
    "buenos dias": "{user} Buenos dias desde {place}",
    "buongiorno": "{user} Boungiorno da {place}",
    "bom dia": "{user} Bom dia de {place}",
    # Arabic
    "sabah al-khair": "{user} Sabah alkhayr min {place}",
    # Other
    "bonan matenon": "{user} Bonan matenon de {place}",
    "sawubona": "{user} Sawubona kusuka {place}",
    "ahayo": "{user} Subax wanaagsan {place}"
}


def read_json_file(filename):
    """
    Reads Json file

    Parameters:
        filename (string) : filename of json file to be read

    Returns:
        list timezones and nested list of location strings
    """
    with open(filename, "r", encoding='UTF-8') as read_file:
        data = json.load(read_file)
        return data


places = read_json_file("place.json")


def get_places():
    """
    Gets the places list

    Returns:
        list timezones and nested list of location strings
    """
    return places


def calculate_timezone(now, target):
    """
    Calculates the calculates the timezone offset between the current time and the target time

    Parameters:
        now (timedate) : the current datetime
        target (timedate) : target datetime

    Returns:
        int: timezone for target time
    """

    timezone = 0

    if now < target:
        while now != target:
            now = now + timedelta(hours=1)
            timezone += 1
    elif now > target:
        while now != target:
            now = now - timedelta(hours=1)
            timezone -= 1
    elif now == target:
        timezone = 0

    if timezone < -12:
        timezone = timezone + 25
    if timezone > 12:
        timezone = timezone - 25
    print(timezone)

    return timezone


def get_location(timezone, index):
    """
    Gets the location string for the timezone

    Parameters:
        timezone (int) : timezone for string
        index (int) : index location item to select

    Returns:
        int: timezone offset between inputs
    """
    for place in places:
        if place["timezone"] == timezone:
            return place["location"][index]
    return None


def morning_in():
    """
    Prints a random location of a list where it is currently 8am in their timezone
    """
    random_location = random.randint(0, 2)

    random_morning = 7 + random.randint(0, 2)

    # Gets the current time and sets minutes, seconds and microseconds to 0
    now = datetime.now()
    now = now.replace(minute=0, second=0, microsecond=0)
    morning = now.replace(hour=random_morning)

    print(now, ' | ', morning)

    timezone = calculate_timezone(now, morning)

    location = get_location(timezone, random_location)

    return location


def get_language_return_type(message):
    """
    Retrieves the language to respond to the message
    Returns:
        string: trigger
    """
    for trigger in morningTriggers:
        if message.content.lower().__contains__(trigger):
            return (TriggerStatus.Regular, trigger)
        if message.content.lower().__contains__(trigger[::-1]):
            return (TriggerStatus.Reverse, trigger)
    return None

def get_response(message, trigger_values, location):
    """
    Generates an appropriate response to the message
    Returns:
        string: response
    """
    if trigger_values is not None:
        trigger_status = trigger_values[0]
        trigger = trigger_values[1]
        if location is not None:
            if trigger_status == TriggerStatus.Reverse:
                return morningTriggers[trigger].format(
                    user="@{}".format(message.author.name),
                    place=location
                    )[::-1]
            return morningTriggers[trigger].format(
                user=message.author.mention, place=location
                )
    return None

def get_morning_response(message):
    """
    Generates an appropriate response to the message
    Returns:
        string: response
    """
    if not message.author.bot:
        trigger_values = get_language_return_type(message)

        if trigger_values is not None:
            location = morning_in()

            return get_response(message, trigger_values, location)
    return None
