# LoreBot

This a discord bot written in discord.py

It can be used to search lore wikis to retrieve information in game series such as elder scrolls(UESP), or Bioshock, or Nier.

Should mostly be as simple as running LoreBot.py in your cloned repo and downloading the requisite libraries.

Required Libraries:
- discord.py (obviously)
- discord.ext
- requests
- ddgs
- python-dotenv
- google.genai

You will need to create a discord developer application and retrieve its API key, as well as the API key for a Google Gemini service account.

**The way it is set up currently, you can create an .env file that contains the lines:**
DISCORD_TOKEN = ""
GEMINI_API_KEY = ""

I wish you luck, I am a fellow learning dev :D
