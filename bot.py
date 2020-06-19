import os
from dotenv import load_dotenv
from discord.ext import commands

# load environment variables
if os.getenv('DEV') is not None:
    load_dotenv('.env')

# create the bot
bot = commands.Bot(owner_id=196141424318611457, command_prefix=commands.when_mentioned_or('hey mitch '), help_command=None)

# add all the cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# run the bot
bot.run(os.getenv('TOKEN'))
