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
    '''Completes instructions on start
    
    The bot prints that it is working into the terminal output, lists the number of commands synced, or raises an exception if something went wrong.
    Changes presence to Streaming and a message to use the help command
    
    '''
    print("Bot is workin")
    await bot.change_presence(activity=discord.Streaming(name="Use /help to learn how to search with LoreBot", url="https://en.uesp.net/wiki/Main_Page"))
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)} commands.")
    except Exception as e:
        print(e)

@bot.tree.command(name="search")
@app_commands.describe(game = "What game or IP to search for?", topic = "What topic did you have in mind?")
async def search(interaction: discord.Interaction, game: str, topic: str):
    '''Searches for game and topic on google calling the Searcher class's query function, which uses the googlesearch module.
    
    Also calls an implementation of Google's Gemini LLM to provide a brief synopsis on the topic.
    
    Returns:
        A string containing the AI synopsis and url pulled from google
    '''
    await interaction.response.defer()
    await Searcher.query(game, topic)
    await asyncio.sleep(4)
    response = model.generate_content(f"Give a brief 50 word or less synopsis on {topic} from {game}.")
    await interaction.followup.send(f"Here's the lore on {topic}!\n{response.text}{result}")

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    '''Sends usageString, contained in a different document called usage.txt'''
    await interaction.response.send_message(usageString)

bot.run(os.getenv('DISCORD_TOKEN'))