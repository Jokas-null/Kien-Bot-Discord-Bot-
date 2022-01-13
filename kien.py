import os ,discord, youtube_dl
from discord import client
from discord.ext.commands import bot, cog
from dotenv import load_dotenv
from discord.ext import commands
from bot_tools import music

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

kien = commands.Bot(command_prefix='-', intends = discord.Intents.all()) #bot prefix
cogs = [music]

for i in range(len(cogs)):
    cogs[i].setup(kien)



@kien.event
async def on_ready():
    await kien.change_presence(activity = discord.Activity(type = discord.ActivityType.watching, name = "-help"))
    print('Bot running')

kien.run(TOKEN)