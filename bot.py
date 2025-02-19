import json
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
import time

cooldowns = {}  # Track cooldowns per user & command

def is_on_cooldown(user_id, command, cooldown_time):
    """Checks if a user is on cooldown for a specific command."""
    now = time.time()
    if user_id in cooldowns and command in cooldowns[user_id]:
        remaining = cooldowns[user_id][command] - now
        if remaining > 0:
            return round(remaining)  # Return remaining cooldown time
    return None  # No cooldown

def set_cooldown(user_id, command, cooldown_time):
    """Sets a cooldown for a specific user and command."""
    now = time.time()
    if user_id not in cooldowns:
        cooldowns[user_id] = {}
    cooldowns[user_id][command] = now + cooldown_time

scenario_cache = []
current_choices = {}  # Stores choices for current adventure
player_stats = {}  # Stores player stats
PLAYER_FILE = "players.json"

# Function to save player stats to a file
def save_players():
    with open(PLAYER_FILE, "w") as f:
        json.dump(player_stats, f)

# Function to load player stats from a file
def load_players():
    global player_stats
    if os.path.exists(PLAYER_FILE):
        with open(PLAYER_FILE, "r") as f:
            player_stats = json.load(f)
    else:
        player_stats = {}

# Load player data when the bot starts
load_players()

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
        user_id = str(message.author.id)

        if user_id in player_stats:
            await message.channel.send("✅ You are already registered! Use `!stats` to view your stats.")
            return

        # Generate random stats
        player_stats[user_id] = {
            "Strength": random.randint(1, 20),
            "Dexterity": random.randint(1, 20),
            "Intelligence": random.randint(1, 20),
            "HP": 100,
            "history": []
        }
        save_players()

        await message.channel.send(f"{message.author.mention}, you have been registered! Use `!stats` to view your attributes.")

    # 📜 VIEW STATS - !stats
    elif message.content.startswith("!stats"):
        user_id = str(message.author.id)

        if user_id not in player_stats:
            await message.channel.send("❌ You are not registered! Use `!register` to create a character.")
            return
        
        stats = player_stats[user_id]
        stats_message = (
            f"📜 **{message.author.name}'s Stats:**\n"
            f"💪 Strength: {stats.get('Strength', 10)}\n"
            f"🏹 Dexterity: {stats.get('Dexterity', 10)}\n"
            f"🧠 Intelligence: {stats.get('Intelligence', 10)}\n"
            f"❤️ HP: {stats.get('HP', 100)}"
        )
    
        await message.channel.send(stats_message)
    
    # 🎲 DICE ROLL - !roll d20
    if message.content.startswith("!roll d20"):

        # Cooldown System (Prevents spam)
        cooldown_time = 3  # 3-second cooldown for !roll d20
        remaining = is_on_cooldown(user_id, "!roll", cooldown_time)

        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before rolling again.")
            return

        set_cooldown(user_id, "!roll", cooldown_time)

        roll = random.randint(1, 20)  # Generate a random number between 1 and 20
        await message.channel.send(f"🎲 You rolled a **{roll}** (1d20)!")

    # 🏰 ADVENTURE GENERATION - !adventure
    if message.content.startswith("!adventure"):
        # Cooldown System (Prevents spam)
        cooldown_time = 10  # 10-second cooldown for !adventure
        remaining = is_on_cooldown(user_id, "!adventure", cooldown_time)

        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before using `!adventure` again.")
            return

        set_cooldown(user_id, "!adventure", cooldown_time)


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

        # Cooldown System (Prevents spam)
        cooldown_time = 5  # 5-second cooldown for !choose
        remaining = is_on_cooldown(user_id, "!choose", cooldown_time)

        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before making another choice.")
            return

        set_cooldown(user_id, "!choose", cooldown_time)

        if user_id not in current_choices:
            await message.channel.send("❌ No active adventure! Use `!adventure` first.")
            return

        choice = message.content.split(" ")[1] if len(message.content.split()) > 1 else None

        if choice in current_choices[user_id]:
            chosen_action = current_choices[user_id][choice]

            # ✅ Store the player's choice history
            if user_id not in player_stats:
                player_stats[user_id] = {"strength": 10, "dexterity": 10, "intelligence": 10, "hp": 100, "history": []}
            player_stats[user_id]["history"].append(chosen_action)  # Append choice
            save_players()  # Persist data

            await message.channel.send(f"🔮 You chose: {chosen_action}")
        else:
            await message.channel.send("❓ Please choose a valid option: `!choose 1`, `!choose 2`, or `!choose 3`.")

# Run the bot
client.run(DISCORD_TOKEN)
