import discord
import requests
import urllib3 as urllib
from discord.ext import commands
from googlesearch import search
from bs4 import BeautifulSoup as BS

http = urllib.PoolManager()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

class Searcher(commands):
    def stdgame(game):
        '''Takes game input and standardizes it across naming schemes'''
        if game.lower() == "skyrim" or "morrowind" or "oblivion" or "eso" or "elder scrolls online" or "daggerfall" or "elder scrolls" or "arena" or "the elder scrolls":
            game = "elder scrolls"
            return game
        else:
            return game

    def query(game, topic):
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
    
    def scrapefandom(data):
        soup = BS(data, 'html.parser')
        soup.prettify()
        text = soup.find('div', {"class=\"mw-parser-output\""}).get_text()
    
    def scrapeuesp(data):
        soup = BS(data, 'html.parser')
        soup.prettify()
        text = soup.find('p').get_text()

bot = commands.Bot(command_prefix='/', intents=intents)
@bot.command()
async def search(ctx, game: str, topic: str):
    await ctx.send(f"Searching {game}'s wiki for {topic}.")
    game = Searcher.stdgame(game)
    if game == "elder scrolls":
        resultText = Searcher.scrapeuesp(Searcher.query(game, topic))
    else:
        resultText = Searcher.scrapefandom(Searcher.query(game, topic))
    await ctx.send(f"{resultText[:-1]}\n{Searcher.query().result}")



client.run('token')