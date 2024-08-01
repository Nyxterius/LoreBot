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

    async def query(game, topic):
        '''Takes game and topic input and returns the first search result
        Args:
            game (str): the game that is being searched
            topic (str): the topic that is being searched for
            if game is elder scrolls then searches specifically for a UESP page
        Returns:
            parg (str): first paragraph inside of body in result page
        '''
        if game.lower() == "skyrim" or "morrowind" or "oblivion" or "eso" or "elder scrolls online" or "daggerfall" or "elder scrolls" or "arena" or "the elder scrolls":
            result = search(f"{game} UESP {topic}", tld='co.in', num = 1, stop = 1)
        else:
            result = search(f"{game} {topic}", tld='co.in', num = 1, stop = 1)
        data = requests.get(str(result))
        BS.find() ###TBD

bot = commands.Bot(command_prefix='/', intents=intents)
@bot.command()
async def search(ctx, game: str, topic: str):
    await ctx.send(f"Searching {game}'s wiki for {topic}.")



client.run('token')