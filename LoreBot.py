import discord
import requests
import urllib3 as urllib

http = urllib.PoolManager()

intents = discord.Intents.default
intents.message_content = True

client = discord.Client(intents=intents)





client.run('MTI2ODM1NzczMzU4MTg1Mjc1NQ.GIydvs._4A98XQuKD9uPpK8jG7cS5yETiqynRCPzm-yZM')