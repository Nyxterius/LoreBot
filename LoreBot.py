#discord imports
import discord
from discord import app_commands
from discord.ext import commands
#other imports
from History import requestHistory
import requests
import urllib3 as urllib
from ddgs import DDGS
from dotenv import load_dotenv
import os
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import asyncio

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

http = urllib.PoolManager()
intents = discord.Intents(messages=True)
intents.message_content = True
intents.typing = False
intents.presences = False
client = discord.Client(intents=intents)

rq = requestHistory()

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
        results = {}
        if game.lower() == "the elder scrolls":
            results = DDGS().text(f"{game} UESP {topic}", region='us-en', safesearch='off', timelimit='y', page=1, backend="google", max_results=1)
        else:
            results = DDGS().text(f"{game} {topic} wiki", region='us-en', safesearch='off', timelimit='y', page=1, backend="google", max_results=1)
        result = results[0]['href']
        return result

class questionQuery():
    def who(game, action):
        response = model.generate_content(f"Who was the character that {action} in {game}?")
        return response

    def when(game, thing, inLore = "True"):
        if inLore.lower() == "true":
            response = model.generate_content(f"When did {thing} happen in/to {game}? 200 words or less.", safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH
    })
            return response
        else:
            response = model.generate_content(f"When was {thing} added to {game}? 200 words or less.", safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH
    })
            return response

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
    await asyncio.sleep(2)
    response = model.generate_content(f"Give a general, approximately 30 word synopsis on {topic} from {game}.", safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH
    })
    rq.store(game, topic, response.text, result)
    await interaction.followup.send(f"Here's the lore on {topic}!\n{response.text}{result}")

@bot.tree.command(name="whodunnit")
@app_commands.describe(game = "What game or IP?", action = "What did they do?")
async def who(interaction: discord.Interaction, game: str, action: str):
    await interaction.response.defer()
    await asyncio.sleep(3)
    response = questionQuery.who(game, action)
    await interaction.followup.send(f"**This is who I think {action}**\n{response.text}")

@bot.tree.command(name="whendidithappen")
@app_commands.describe(game = "What game or IP?", thing = "What thing are you asking about?", lore = "True/False")
async def when(interaction: discord.Interaction, game: str, thing: str, lore: str):
    await interaction.response.defer()
    await asyncio.sleep(3)
    response = questionQuery.when(game, thing, lore)
    await interaction.followup.send(f"**This is what I think happened**\n{response.text}")

@bot.tree.command(name="lorelonger")
@app_commands.describe(game = "What game or IP?", topic = "What topic did you have in mind?")
async def lorelonger(interaction: discord.Interaction, game: str, topic: str):
    await interaction.response.defer()
    await asyncio.sleep(3)
    response = model.generate_content(f"Provide a comprehensive summary of all lore on {topic} from {game} between 1000 and 1900 characters in length. Do not restate output length in response.", safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH
    })
    await interaction.followup.send(f"Here's all of the lore I know on {topic}!\n{response.text}")

@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    '''Sends usageString, contained in a different document called usage.txt'''
    await interaction.response.send_message(usageString)

@bot.tree.command(name="history")
async def history(interaction: discord.Interaction):
    '''Sends cross-server request history! History list resets every 6 entries'''
    await interaction.response.send_message(rq.returnHistory())

bot.run(os.getenv('DISCORD_TOKEN'))
