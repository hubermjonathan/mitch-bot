import os
from dotenv import load_dotenv
from discord.ext import commands

# load environment variables
if os.getenv('DEV') is not None:
    load_dotenv('.env')

# create the bot
bot = commands.Bot(owner_id=196141424318611457, command_prefix=commands.when_mentioned, help_command=None)

# add all the cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# add the error logger
@bot.event
async def on_command_error(ctx, error):
    print(f'BOT ERROR: {error}')

# run the bot
bot.run(os.getenv('TOKEN'))
