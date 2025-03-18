import platform
import discord
import json
import os
import asyncio
import time
from colorama import Fore, Back, Style
from discord.ext import commands
from discord import app_commands

# Define intents
bot = commands.Bot(command_prefix='-',intents = discord.Intents.all())

@bot.event
async def on_message(message):
    if message.author != bot.user:
        print(f'Received message: {message.content}')
        await bot.process_commands(message)  # Assicurati di chiamare questa linea per gestire i comandi

@bot.event
async def on_ready():
    prefisso=(time.strftime("%H:%M:%S", time.localtime()))
    syn=await bot.tree.sync()
    myStr=(f"{prefisso} Collegato come {bot.user.name}\n {prefisso} Discord Py Version {discord.__version__}\n {prefisso} Python Version {str(platform.python_version())}\n {prefisso} Running on {str(len(syn))} slash commands\n {prefisso} Running on {str(len(bot.guilds))} servers")
    print(myStr)
    await bot.change_presence(activity=discord.Game(name='!help'))

#initialise the cogs
async def load_cogs():
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'Cogs.{filename[:-3]}')

# bot starter
async def main():
    async with bot:
        await load_cogs()
        await bot.start(config['Token'])
        
# Load the config file
with open('config.json','r') as f:
    config = json.load(f)
  
asyncio.run(main())
