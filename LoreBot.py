#discord imports
import discord
from discord import app_commands
from discord.ext import commands
import requests
#other imports
import urllib3 as urllib
from googlesearch import search
from bs4 import BeautifulSoup as BS
from dotenv import load_dotenv
import os

http = urllib.PoolManager()

intents = discord.Intents(messages=True)
intents.message_content = True
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

class Searcher():
    async def stdgame(game):
        '''Takes game input and standardizes it across naming schemes'''
        if game.lower() == "skyrim" or "morrowind" or "oblivion" or "eso" or "elder scrolls online" or "daggerfall" or "elder scrolls" or "arena" or "the elder scrolls":
            game = "elder scrolls"
            return game
        else:
            return game

    async def query(game, topic):
        '''Takes game and topic input and returns the first search result
        Args:
            game (str): the game that is being searched
            topic (str): the topic that is being searched for
            if game is elder scrolls then searches specifically for a UESP page
        Returns:
            parg (str): first paragraph inside of body in result page
        '''
        if game == "elder scrolls":
            result = search(f"{game} UESP {topic}", tld='co.in', num = 1, stop = 1)
        else:
            result = search(f"{game} {topic}", tld='co.in', num = 1, stop = 1)
        data = requests.get(str(result))
        return data
    
    async def scrapefandom(data):
        soup = BS(data, 'html.parser')
        soup.prettify()
        text = soup.find('div', {"class=\"mw-parser-output\""}).get_text()
    
    async def scrapeuesp(data):
        soup = BS(data, 'html.parser')
        soup.prettify()
        text = soup.find('p').get_text()


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
    await interaction.response.send_message(f"Searching {game}'s wiki for {topic}.")
    game = Searcher.stdgame(game)
    if game == "elder scrolls":
        resultText = Searcher.scrapeuesp(Searcher.query(game, topic))
    else:
        resultText = Searcher.scrapefandom(Searcher.query(game, topic))
    await interaction.response.send_message(f"{str(resultText)[:-1]}\n{Searcher.query().result}")

bot.run(os.getenv('DISCORD_TOKEN'))