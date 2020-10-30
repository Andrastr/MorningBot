from datetime import timedelta
import json


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


def get_language_return_type(message, morningTriggers):
    """
    Retrieves the language to respond to the message
    Returns:
        int: index of the response message
    """
    index = 0
    for inputLanguage in morningTriggers:
        if message.content.lower().__contains__(inputLanguage):
            return index
        index += 1
