import json
import os
import discord
import asyncio
import random
import re
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Client
client_ai = OpenAI(api_key=OPENAI_API_KEY)  # New API structure
def generate_ai_response(prompt, model="gpt-3.5-turbo"):
    """Generate AI response using the selected model (default: GPT-3.5-Turbo)."""
    try:
        response = client_ai.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are a Dungeon Master generating D&D content."},
                      {"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error with OpenAI API: {e}")
        return "⚠️ AI response error. Try again later."


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

scenario_cache = {}  # Stores AI-generated adventures along with timestamps
CACHE_EXPIRY_TIME = 300  # Cache expires after 300 seconds (5 minutes)
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
    elif message.content.startswith("!adventure"):
        user_id = str(message.author.id)
        
        # Cooldown System (Prevents spam)
        cooldown_time = 10  # 10-second cooldown for !adventure
        remaining = is_on_cooldown(user_id, "!adventure", cooldown_time)

        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before using `!adventure` again.")
            return

        set_cooldown(user_id, "!adventure", cooldown_time)


        # Check if a cached scenario exists and is still valid
        current_time = time.time()
        if user_id in scenario_cache:
            cached_entry = scenario_cache[user_id]
            if (current_time - cached_entry["timestamp"]) < CACHE_EXPIRY_TIME:
                # Retrieve cached adventure data
                adventure_text = cached_entry["adventure_text"]
                choices = cached_entry["choices"] # Choices were stored in a list format

                # **Fix Choice Formatting when Reusing Cache**
                choice_dict = {str(i + 1): choices[i] for i in range(len(choices))}
                current_choices[user_id] = choice_dict  # Ensure choices are properly tracked

                formatted_choices = "\n".join([f"{i+1}️⃣ {choices[i]}" for i in range(len(choices))])

                adventure_message = (
                    f"♻️ Using a recent adventure:\n\n"
                    f"📜 **Adventure Hook:**\n{adventure_text}\n\n"
                    f"⚔️ **Choices:**\n"
                    f"{formatted_choices}\n\n"
                    f"Use `!choose 1`, `!choose 2`, or `!choose 3` to decide your action!"
                )

                await message.channel.send(adventure_message)
                return # Stop here if using cache
            else:
                # Cache expired, remove it
                del scenario_cache[user_id]
        
        # Otherwise, generate a new adventure
        await message.channel.send("🎲 Generating a new adventure... please wait!")
        
        prompt = "Generate a short D&D adventure hook with three choices."
        scenario = generate_ai_response(prompt, model="gpt-3.5-turbo")

        # Format the scenario and choices
        scenario_lines = scenario.split("\n")
        adventure_text = []
        extracted_choices = []

        # Detects numbered choices formatted as "1. ", "2. ", "3. " etc.
        choice_pattern = re.compile(r"^\d+\.\s*(.*)")

        for line in scenario_lines:
            match = choice_pattern.match(line.strip())
            if match:
                extracted_choices.append(match.group(1).strip())
            else:
                adventure_text.append(line.strip())

        # Debugging: Print extracted choices
        print(f"DEBUG: Extracted Choices: {extracted_choices}")
        print(f"DEBUG: current_choices before assignment: {current_choices}")

        # Join adventure text while ensuring blank lines remain correct
        adventure_text = "\n".join(adventure_text).strip()

        # Store choices in a user-specific dictionary
        choice_dict = {}
        for i, choice in enumerate(extracted_choices, 1):
            if choice:  # Ensure it's not an empty string
                choice_dict[str(i)] = choice
        current_choices[user_id] = choice_dict

        formatted_choices = "\n".join([f"{i}️⃣ **{choice}**" for i, choice in enumerate(extracted_choices, 1)])

        adventure_message = (
            f"📜 **Adventure Hook:**\n{adventure_text}\n\n"
            f"⚔️ **Choices:**\n{formatted_choices}\n\n"
            f"Use `!choose 1`, `!choose 2`, or `!choose 3` to decide your action!"
        )

        # **Update Cache with Expiration**
        scenario_cache[user_id] = {
            "adventure_text": adventure_text,  # Store adventure description
            "choices": extracted_choices,  # Store choices separately
            "timestamp": current_time
        }

        await message.channel.send(adventure_message)

    # 🚀 PLAYER MAKES A CHOICE - !choose 1/2/3
    
    elif message.content.startswith("!choose"):
        user_id = str(message.author.id)  # Ensure consistency

        print(f"DEBUG: current_choices: {current_choices}")
        print(f"DEBUG: current_choices[{user_id}]: {current_choices.get(user_id, 'Not Found')}")

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

        choice = str(message.content.split(" ")[1]) if len(message.content.split()) > 1 else None
        print(f"DEBUG: current_choices[{user_id}] = {current_choices.get(user_id, 'Not Found')}")

        if choice in current_choices[user_id]:
            
            chosen_action = current_choices[user_id][choice]
            print(f"DEBUG: chosen_action before sending: {chosen_action}")

            # ✅ Store the player's choice history
            if user_id not in player_stats:
                player_stats[user_id] = {"strength": 10, "dexterity": 10, "intelligence": 10, "hp": 100, "history": []}
            player_stats[user_id]["history"].append(chosen_action)  # Append choice
            save_players()  # Persist data

            # 🎲 Modify outcome based on dice roll and stats using GPT-4
            dice_result = random.randint(1, 20)
            prompt = f"""
            The player has chosen: {chosen_action}.
            Their d20 roll result was {dice_result}.
            Given the adventure context, generate a dynamic outcome based on this result.
            """

            outcome = generate_ai_response(prompt, model="gpt-4")


            await message.channel.send(f"🔮 You chose: {chosen_action}\n🎲 Your roll: {dice_result}\n📝 **Outcome:** {outcome}")
        else:
            await message.channel.send("❓ Please choose a valid option: `!choose 1`, `!choose 2`, or `!choose 3`.")

# Run the bot
client.run(DISCORD_TOKEN)
