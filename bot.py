import json
import os
import discord
import asyncio
import random
import re
import time
from openai import OpenAI
from dotenv import load_dotenv
import sqlite3

# Database file for decision tracking
DB_FILE = "decisions.db"

def init_db():
    """
    Initialize the SQLite database and create the 'decisions' table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            decision TEXT NOT NULL,
            adventure_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def log_decision(user_id, decision, adventure_text=""):
    """
    Log a player's decision into the database.
    
    Args:
        user_id (str): The player's unique ID.
        decision (str): The chosen decision text.
        adventure_text (str): The adventure hook context (optional).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO decisions (user_id, decision, adventure_text)
        VALUES (?, ?, ?)
    ''', (user_id, decision, adventure_text))
    conn.commit()
    conn.close()


# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client_ai = OpenAI(api_key=OPENAI_API_KEY)

def generate_ai_response(prompt, model="gpt-3.5-turbo"):
    """
    Generate an AI response using the specified model.
    Default model is GPT-3.5-Turbo, but can be set to GPT-4 for decision outcomes.
    """
    try:
        response = client_ai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a Dungeon Master generating D&D content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error with OpenAI API: {e}")
        return "⚠️ AI response error. Try again later."

# Set up Discord bot intents and initialize the client
intents = discord.Intents.default()
intents.message_content = True  # Allow the bot to read message content
client = discord.Client(intents=intents)

# ------------------ Cooldown and Caching Setup ------------------

# Dictionary to track cooldowns for each user and command
cooldowns = {}

def is_on_cooldown(user_id, command, cooldown_time):
    """
    Check if a user is on cooldown for a specific command.
    Returns the remaining cooldown time (in seconds) if applicable.
    """
    now = time.time()
    if user_id in cooldowns and command in cooldowns[user_id]:
        remaining = cooldowns[user_id][command] - now
        if remaining > 0:
            return round(remaining)
    return None

def set_cooldown(user_id, command, cooldown_time):
    """
    Set a cooldown for a specific user and command.
    """
    now = time.time()
    if user_id not in cooldowns:
        cooldowns[user_id] = {}
    cooldowns[user_id][command] = now + cooldown_time

# Cache for AI-generated adventures and current choices tracking
scenario_cache = {}        # Stores adventures with timestamps
CACHE_EXPIRY_TIME = 300      # Cache expiry time in seconds (5 minutes)
current_choices = {}         # Stores the current adventure choices for each user

# ------------------ Player Data Management ------------------

player_stats = {}           # Dictionary to hold player stats and history
PLAYER_FILE = "players.json"

def save_players():
    """
    Save the current player stats to a JSON file.
    """
    with open(PLAYER_FILE, "w") as f:
        json.dump(player_stats, f)

def load_players():
    """
    Load player stats from a JSON file if it exists.
    """
    global player_stats
    if os.path.exists(PLAYER_FILE):
        with open(PLAYER_FILE, "r") as f:
            player_stats = json.load(f)
    else:
        player_stats = {}

# Load player data when the bot starts
load_players()

# ------------------ Discord Bot Event Handlers ------------------

@client.event
async def on_ready():
    """
    Event handler for when the bot successfully logs in.
    """
    init_db()  # Initialize the decision tracking database
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    """
    Main event handler for incoming messages.
    Handles commands: !register, !stats, !roll d20, !adventure, and !choose.
    """
    if message.author == client.user:
        return  # Ignore messages sent by the bot itself

    user_id = message.author.id

    # ----- PLAYER REGISTRATION: !register -----
    if message.content.startswith("!register"):
        user_id_str = str(message.author.id)
        if user_id_str in player_stats:
            await message.channel.send("✅ You are already registered! Use `!stats` to view your stats.")
            return

        # Generate random ability scores for a full D&D 5e character
        ability_scores = {
            "Strength": random.randint(1, 20),
            "Dexterity": random.randint(1, 20),
            "Constitution": random.randint(1, 20),
            "Intelligence": random.randint(1, 20),
            "Wisdom": random.randint(1, 20),
            "Charisma": random.randint(1, 20)
        }
        # Calculate Constitution modifier using (Constitution - 10) // 2
        con_modifier = (ability_scores["Constitution"] - 10) // 2
        # Set HP to a base value (10) plus the Constitution modifier; ensure minimum HP is 1
        hp = max(10 + con_modifier, 1)

        player_stats[user_id_str] = {
            **ability_scores,
            "HP": hp,
            "history": []
        }
        save_players()
        await message.channel.send(f"{message.author.mention}, you have been registered! Use `!stats` to view your attributes.")

    # ----- VIEW PLAYER STATS: !stats -----
    elif message.content.startswith("!stats"):
        user_id_str = str(message.author.id)
        if user_id_str not in player_stats:
            await message.channel.send("❌ You are not registered! Use `!register` to create a character.")
            return

        stats = player_stats[user_id_str]

        # Function to calculate the ability modifier
        def calc_modifier(score):
            return (score - 10) // 2

        stats_message = (
            f"📜 **{message.author.name}'s Stats:**\n"
            f"💪 Strength: {stats.get('Strength', 10)} (mod: {calc_modifier(stats.get('Strength', 10)):+})\n"
            f"🏹 Dexterity: {stats.get('Dexterity', 10)} (mod: {calc_modifier(stats.get('Dexterity', 10)):+})\n"
            f"🛡️ Constitution: {stats.get('Constitution', 10)} (mod: {calc_modifier(stats.get('Constitution', 10)):+})\n"
            f"🧠 Intelligence: {stats.get('Intelligence', 10)} (mod: {calc_modifier(stats.get('Intelligence', 10)):+})\n"
            f"👁️ Wisdom: {stats.get('Wisdom', 10)} (mod: {calc_modifier(stats.get('Wisdom', 10)):+})\n"
            f"🗣️ Charisma: {stats.get('Charisma', 10)} (mod: {calc_modifier(stats.get('Charisma', 10)):+})\n"
            f"❤️ HP: {stats.get('HP', 10)}"
        )
        await message.channel.send(stats_message)
    
    # 🎲 DICE ROLL - !roll d20 with stat bonus integration
    if message.content.startswith("!roll d20"):
        cooldown_time = 3  # 3-second cooldown for !roll d20
        remaining = is_on_cooldown(user_id, "!roll", cooldown_time)
        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before rolling again.")
            return

        set_cooldown(user_id, "!roll", cooldown_time)
        roll = random.randint(1, 20)  # Generate a random d20 roll

        # Parse command arguments: expected format is "!roll d20 [ability]"
        parts = message.content.split()

        # If no additional parameter is provided, just output the raw roll
        if len(parts) == 2:
            await message.channel.send(f"🎲 You rolled a **{roll}** (1d20) with no modifier!")
            return

        # If an ability parameter is provided, validate and apply its modifier
        ability = parts[2].capitalize()
        if ability not in {"Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"}:
            await message.channel.send("❌ Invalid ability specified. Choose from Strength, Dexterity, Constitution, Intelligence, Wisdom, or Charisma.")
            return

        user_id_str = str(message.author.id)
        if user_id_str in player_stats:
            # Retrieve the ability score and calculate its modifier
            score = player_stats[user_id_str].get(ability, 10)
            bonus = (score - 10) // 2
            final_total = roll + bonus
            bonus_str = f" (+{bonus})" if bonus >= 0 else f" ({bonus})"
            await message.channel.send(
                f"🎲 You rolled a **{roll}**{bonus_str} (1d20) using your {ability} modifier for a total of **{final_total}**!"
            )
        else:
            await message.channel.send(
                f"🎲 You rolled a **{roll}** (1d20)! Register with `!register` to gain stat bonuses."
            )


    # ----- ADVENTURE GENERATION: !adventure -----
    elif message.content.startswith("!adventure"):
        user_id_str = str(message.author.id)
        cooldown_time = 10  # 10-second cooldown for adventure generation
        remaining = is_on_cooldown(user_id, "!adventure", cooldown_time)
        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before using `!adventure` again.")
            return

        set_cooldown(user_id, "!adventure", cooldown_time)
        current_time = time.time()

        # Check if there's a valid cached adventure
        if user_id_str in scenario_cache:
            cached_entry = scenario_cache[user_id_str]
            if (current_time - cached_entry["timestamp"]) < CACHE_EXPIRY_TIME:
                adventure_text = cached_entry["adventure_text"]
                choices = cached_entry["choices"]
                # Format cached choices into a dictionary and update current choices
                choice_dict = {str(i + 1): choices[i] for i in range(len(choices))}
                current_choices[user_id_str] = choice_dict

                formatted_choices = "\n".join([f"{i+1}️⃣ {choices[i]}" for i in range(len(choices))])
                adventure_message = (
                    f"♻️ Using a recent adventure:\n\n"
                    f"📜 **Adventure Hook:**\n{adventure_text}\n\n"
                    f"⚔️ **Choices:**\n{formatted_choices}\n\n"
                    f"Use `!choose 1`, `!choose 2`, or `!choose 3` to decide your action!"
                )
                await message.channel.send(adventure_message)
                return  # Stop further processing if using cached adventure
            else:
                # Remove expired cache entry
                del scenario_cache[user_id_str]

        # Generate a new adventure if no valid cache exists
        await message.channel.send("🎲 Generating a new adventure... please wait!")
        prompt = "Generate a short D&D adventure hook with three choices."
        scenario = generate_ai_response(prompt, model="gpt-3.5-turbo")

        # Parse the AI-generated scenario into adventure text and choices
        scenario_lines = scenario.split("\n")
        adventure_text_lines = []
        extracted_choices = []
        choice_pattern = re.compile(r"^\d+\.\s*(.*)")  # Matches choices like "1. Choice text"

        for line in scenario_lines:
            match = choice_pattern.match(line.strip())
            if match:
                extracted_choices.append(match.group(1).strip())
            else:
                adventure_text_lines.append(line.strip())

        adventure_text = "\n".join(adventure_text_lines).strip()

        # Store the choices in a dictionary and update current choices
        choice_dict = {str(i): choice for i, choice in enumerate(extracted_choices, 1) if choice}
        current_choices[user_id_str] = choice_dict

        formatted_choices = "\n".join([f"{i}️⃣ **{choice}**" for i, choice in enumerate(extracted_choices, 1)])
        adventure_message = (
            f"📜 **Adventure Hook:**\n{adventure_text}\n\n"
            f"⚔️ **Choices:**\n{formatted_choices}\n\n"
            f"Use `!choose 1`, `!choose 2`, or `!choose 3` to decide your action!"
        )

        # Cache the newly generated adventure
        scenario_cache[user_id_str] = {
            "adventure_text": adventure_text,
            "choices": extracted_choices,
            "timestamp": current_time
        }
        await message.channel.send(adventure_message)

    # ----- PLAYER MAKES A CHOICE: !choose 1/2/3 -----
    elif message.content.startswith("!choose"):
        user_id_str = str(message.author.id)
        cooldown_time = 5  # 5-second cooldown for making a choice
        remaining = is_on_cooldown(user_id, "!choose", cooldown_time)
        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before making another choice.")
            return

        set_cooldown(user_id, "!choose", cooldown_time)

        # Ensure there is an active adventure for the user
        if user_id_str not in current_choices:
            await message.channel.send("❌ No active adventure! Use `!adventure` first.")
            return

        # Extract the choice number from the message
        parts = message.content.split()
        choice = parts[1] if len(parts) > 1 else None

        if choice in current_choices[user_id_str]:
            chosen_action = current_choices[user_id_str][choice]

            # Append the chosen action to the player's history and save the update
            if user_id_str not in player_stats:
                # In case the player isn't registered, initialize default stats
                player_stats[user_id_str] = {
                    "Strength": 10, "Dexterity": 10, "Constitution": 10,
                    "Intelligence": 10, "Wisdom": 10, "Charisma": 10,
                    "HP": 10, "history": []
                }
            player_stats[user_id_str]["history"].append(chosen_action)
            save_players()

            # Retrieve the adventure text from cache (if available)
            adventure_text = ""
            if user_id_str in scenario_cache:
                adventure_text = scenario_cache[user_id_str].get("adventure_text", "")

            # Log the decision into the SQLite database
            log_decision(user_id_str, chosen_action, adventure_text)

            # Roll a d20 and use GPT-4 to generate a dynamic outcome based on the choice
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

# ------------------ Run the Discord Bot ------------------

client.run(DISCORD_TOKEN)
