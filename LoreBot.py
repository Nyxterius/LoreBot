import discord
import requests
import urllib3 as urllib

http = urllib.PoolManager()

intents = discord.Intents.default
intents.message_content = True

client = discord.Client(intents=intents)





client.run('token')