#discord imports
import discord
from discord import app_commands
from discord.ext import commands
import requests
#other imports
import urllib3 as urllib
from googlesearch import lucky as gsearch
from bs4 import BeautifulSoup as BS
from dotenv import load_dotenv
import os
import google.generativeai as genai
import asyncio

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

http = urllib.PoolManager()
intents = discord.Intents(messages=True)
intents.message_content = True
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

with open('usage.txt') as usage:
    usageString = usage.read()

class Searcher():
    async def query(game, topic):
        '''Takes game and topic input and returns the first search result
        Args:
            game (str): the game that is being searched
            topic (str): the topic that is being searched for
            if game is elder scrolls then searches specifically for a UESP page
        Returns:
            result (str): url of the website
        '''
        global result
        result = ""
        if game.lower() == "the elder scrolls":
            result = gsearch(f"{game} UESP {topic}", tld='com', lang='en')
        else:
            result = gsearch(f"{game} {topic} wiki", tld='com', lang='en')
        data = requests.get(str(result))
        return data


bot = commands.Bot(command_prefix='?', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is workin")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commands.")
    except Exception as e:
        print(e)

@bot.tree.command(name="search")
@app_commands.describe(game = "What game or IP to search for?", topic = "What topic did you have in mind?")
async def search(interaction: discord.Interaction, game: str, topic: str):
    await interaction.response.defer()
    await Searcher.query(game, topic)
    await asyncio.sleep(4)
    response = model.generate_content(f"Give a brief 50 word or less synopsis on {topic} from {game}.")
    await interaction.followup.send(f"Here's the lore on {topic}!\n{response.text}{result}")

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(usageString)

bot.run(os.getenv('DISCORD_TOKEN'))