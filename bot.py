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
current_choices = {}  # Stores choices for current adventure
player_stats = {}  # Stores player stats

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore bot's own messages

    user_id = message.author.id

    # 📜 PLAYER REGISTRATION - !register
    if message.content.startswith("!register"):
        if user_id in player_stats:
            await message.channel.send("✅ You are already registered! Use `!stats` to view your stats.")
            return

        # Generate random stats (later we can allow customization)
        player_stats[user_id] = {
            "Strength": random.randint(1, 20),
            "Dexterity": random.randint(1, 20),
            "Intelligence": random.randint(1, 20),
            "HP": 100
        }

        await message.channel.send(
            f"🎭 **Character Registered!**\n"
            f"💪 Strength: {player_stats[user_id]['Strength']}\n"
            f"🏃 Dexterity: {player_stats[user_id]['Dexterity']}\n"
            f"🧠 Intelligence: {player_stats[user_id]['Intelligence']}\n"
            f"❤️ HP: {player_stats[user_id]['HP']}"
        )
    
    # 📜 VIEW STATS - !stats
    elif message.content.startswith("!stats"):
        if user_id not in player_stats:
            await message.channel.send("❌ You are not registered! Use `!register` to create a character.")
            return
        
        stats = player_stats[user_id]
        await message.channel.send(
            f"📜 **Your Stats:**\n"
            f"💪 Strength: {stats['Strength']}\n"
            f"🏃 Dexterity: {stats['Dexterity']}\n"
            f"🧠 Intelligence: {stats['Intelligence']}\n"
            f"❤️ HP: {stats['HP']}"
        )

    # 🎲 DICE ROLL - !roll d20
    elif message.content.startswith("!roll d20"):
        roll = random.randint(1, 20)  # Generate a random number between 1 and 20
        await message.channel.send(f"🎲 You rolled a **{roll}** (1d20)!")

    # 🏰 ADVENTURE GENERATION - !adventure
    elif message.content.startswith("!adventure"):
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
                        {"role": "user", "content": "Generate a new adventure hook with three distinct choices."}
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

        # Extract the scenario and choices dynamically
        scenario_lines = [line.strip() for line in scenario.split("\n") if line.strip()]  # Remove blank lines
        adventure_text = "\n".join(scenario_lines[:-3])  # Keep everything except the last 3 lines
        choices = scenario_lines[-3:]

        # Clean up choices to ensure they start correctly
        choices = [choice.lstrip("123. ") for choice in choices] 

        choice_dict = {str(i + 1): choice for i, choice in enumerate(choices)}
        current_choices[user_id] = choice_dict  # Store choices for this player

        adventure_message = f"📝 **Adventure Hook:**\n{adventure_text}\n\n" \
                            f"⚔️ Choices:\n" \
                            f"1️⃣ {choices[0]}\n" \
                            f"2️⃣ {choices[1]}\n" \
                            f"3️⃣ {choices[2]}\n\n" \
                            f"Use `!choose 1`, `!choose 2`, or `!choose 3` to decide your action!"

        await message.channel.send(adventure_message)

    # 🚀 PLAYER MAKES A CHOICE - !choose 1/2/3
    elif message.content.startswith("!choose"):
        if user_id not in current_choices:
            await message.channel.send("❌ No active adventure! Use `!adventure` first.")
            return

        choice = message.content.split(" ")[1] if len(message.content.split()) > 1 else None

        if choice in current_choices[user_id]:
            await message.channel.send(f"🔮 You chose: {current_choices[user_id][choice]}")
        else:
            await message.channel.send("❓ Please choose a valid option: `!choose 1`, `!choose 2`, or `!choose 3`.")

# Run the bot
client.run(DISCORD_TOKEN)
