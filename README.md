# LoreBot

This a discord bot written in discord.py

It can be used to search lore wikis to retrieve information in game series such as elder scrolls(UESP), or Bioshock, or Nier.

Should mostly be as simple as running LoreBot.py in your cloned repo and downloading the requisite libraries.

Required Libraries:
- discord.py (obviously)
- discord.ext
- requests
- urllib3
- google
- python-dotenv
- google.generativeai
- os
- asyncio

You will need to create a discord developer application and retrieve its API key, as well as the API key for a Google Gemini service account.

**The way it is set up currently, you can create an additional file in your directory called .env that contains the lines:**
DISCORD_TOKEN = ""
GEMINI_API_KEY = ""
*I would recommend adding .env to your .gitignore file, so that you don't leak your API keys*

I wish you luck, I am a fellow learning dev :D