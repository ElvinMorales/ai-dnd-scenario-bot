import os
import discord
import asyncio
import random
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client_ai = OpenAI(api_key=OPENAI_API_KEY)  # New API structure

# Set up Discord bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages
client = discord.Client(intents=intents)

# Cooldown & Response Cache
cooldowns = {}
scenario_cache = []

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore bot's own messages

    user_id = message.author.id

    if message.content.startswith("!adventure"):
        # Cooldown System (Prevents spam)
        if user_id in cooldowns and cooldowns[user_id] > asyncio.get_event_loop().time():
            await message.channel.send("⏳ Please wait a few seconds before requesting another adventure.")
            return
        cooldowns[user_id] = asyncio.get_event_loop().time() + 10  # 10-second cooldown

        # Use Cached Response If Available
        if scenario_cache:
            scenario = random.choice(scenario_cache)
        else:
            try:
                response = client_ai.chat.completions.create(
                    model="gpt-3.5-turbo",  # Lower cost model
                    messages=[
                        {"role": "system", "content": "You are a Dungeon Master. Generate a BRIEF D&D adventure hook with a challenge and three choices."},
                        {"role": "user", "content": "Generate a new adventure hook."}
                    ],
                    temperature=0.7  # Balanced randomness
                )
                scenario = response.choices[0].message.content
                scenario_cache.append(scenario)  # Store in cache

                # Limit Cache Size to Avoid Memory Overload
                if len(scenario_cache) > 5:
                    scenario_cache.pop(0)

            except Exception as e:
                print(f"❌ Error with OpenAI API: {e}")
                await message.channel.send("⚠️ Error generating adventure. Please try again later.")
                return

        # Send the Scenario Response
        await message.channel.send(f"📝 **Adventure Hook:**\n{scenario}")

# Run the bot
client.run(DISCORD_TOKEN)
