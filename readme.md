# Morning Bot

Here at Joel Adams & Co. engineering we pride ourselves in creating revolutionary new 
inventions such as this discord bot. Why are you still reading this? Go add it 
already!

## Testing install instructions`

Run `pipenv install` into the terminal

Run `pipenv shell` to enter pip environment

Create .env file like bellow:

```conf
# .env
DISCORD_TOKEN=YOUR_TOKEN_HERE
```

Replacing YOUR_TOKEN_HERE with the token for your bot, see <https://discordpy.readthedocs.io/en/latest/discord.html> for how to get that.

Run in console via running `python morningbot.py`

If is correct it should output :

`<Your bot name> has connected to Discord!`

To test see <https://discordpy.readthedocs.io/en/latest/discord.html> on how to add bot to a server.

## Running Unit tests

To run the unit test run python testMorningbot.py with Pipenv shell
