from discord.ext import commands
from discord.ext.commands import Context

import logging

kitchenQueue = {'nothing': []}
bathroomQueue = {'nothing': []}


def setup(bot):
    """
    Setup the cogs in this extension
    """
    bot.add_cog(Queue(bot))


def getKitchenQueue(serverName: str):
    """
    Get the kitchen queue for the server
    """
    if serverName in kitchenQueue.keys():
        return kitchenQueue.get(serverName)
    else:
        kitchenQueue[serverName] = []
        return kitchenQueue.get(serverName)


def getBathroomQueue(serverName: str):
    """
    Get the bathroom queue for the server
    """
    if serverName in bathroomQueue.keys():
        return bathroomQueue.get(serverName)
    else:
        bathroomQueue[serverName] = []
        return bathroomQueue.get(serverName)


class Queue(commands.Cog):
    """
    Commands for house
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def use(self, ctx: Context, arg):
        """
        Adds the person to the kitchen(k) or bathroom(b) queue
        """
        s = ctx.message.author

        if arg == "k":
            q = getKitchenQueue(ctx.guild)
            name = "kitchen"
        elif arg == "b":
            q = getBathroomQueue(ctx.guild)
            name = "bathroom"
        else:
            raise Exception("Incorrect parameters")

        if len(q) < 1:
            q.append(s)
            logging.info('{0} add {1}'.format(ctx.guild, s))
            await ctx.send(s.mention + ' is now in the ' + name)
        else:
            await ctx.send(q[0].mention + ' is already in the ' + name)

    @commands.command()
    async def done(self, ctx: Context, arg):
        """
        Removes people from the kitchen(k) or bathroom(b) queue
        """
        s = ctx.message.author

        if arg == "k":
            q = getKitchenQueue(ctx.guild)
            name = "kitchen"
        elif arg == "b":
            q = getBathroomQueue(ctx.guild)
            name = "bathroom"
        else:
            raise Exception("Incorrect parameters")

        if s in q:
            q.remove(s)
            logging.info('{0} remove {1}'.format(ctx.guild, s))
            await ctx.send(s.mention + ' is no longer in the ' + name)
        else:
            await ctx.send(s.mention + ' is not in the ' + name)
