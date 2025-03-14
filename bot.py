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
GRAVEYARD_FILE = "graveyard.json"

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

def save_to_graveyard(user_id, character_data):
    """
    Saves deleted character data to a separate file (graveyard.json) before removing it from active play.
    """
    graveyard = {}

    # Load existing graveyard data if the file exists
    if os.path.exists(GRAVEYARD_FILE):
        with open(GRAVEYARD_FILE, "r") as f:
            graveyard = json.load(f)

    # Save the deleted character
    graveyard[user_id] = character_data

    with open(GRAVEYARD_FILE, "w") as f:
        json.dump(graveyard, f, indent=4)

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

    # Predefined fantasy names, races, and classes for random generation
    FANTASY_NAMES = [
        "Aether", "Breeze", "Cinder", "Dawn", "Echo", "Frost", "Glimmer", "Haven",
        "Ink", "Jade", "Kindle", "Lumen", "Mist", "Nova", "Onyx", "Pulse", "Quill",
        "Rune", "Shade", "Tempest", "Umbra", "Veridian", "Whisper", "Xylos", "Yield",
        "Zenith", "Amber", "Blaze", "Cascade", "Drift", "Ember", "Flare", "Gale",
        "Horizon", "Iron", "Journey", "Keystone", "Lunar", "Mirage", "Nexus",
        "Oracle", "Path", "Quartz", "Ripple", "Spark", "Twilight", "Unity",
        "Vortex", "Wisp", "Xenon", "Yearn", "Zeal"
    ]

    RACES = [
        "Dragonborn", "Dwarf", "Elf", "Gnome", "Half-Elf", "Halfling", "Half-Orc", "Human",
        "Tiefling", "Aarakocra", "Aasimar", "Bugbear", "Centaur", "Changeling",
        "Deep Gnome (Svirfneblin)", "Firbolg", "Genasi (Air)", "Genasi (Earth)",
        "Genasi (Fire)", "Genasi (Water)", "Gith (Githyanki)", "Gith (Githzerai)",
        "Goblin", "Goliath", "Grung", "Harengon", "Hobgoblin", "Kalashtar", "Kenku",
        "Kobold", "Lizardfolk", "Loxodon", "Minotaur", "Orc", "Owlin", "Rabbitfolk",
        "Reborn", "Satyr", "Sea Elf", "Shadar-kai", "Shifter", "Simic Hybrid", "Tabaxi",
        "Tortle", "Triton", "Vedalken", "Verdan", "Warforged", "Yuan-ti Pureblood"
    ]

    CLASSES = [
        "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk", "Paladin", "Ranger",
        "Rogue", "Sorcerer", "Warlock", "Wizard", "Artificer"
    ]

    if message.content.startswith("!register"):
        user_id_str = str(message.author.id)

        if user_id_str in player_stats:
            await message.channel.send("✅ You are already registered! Use `!stats` to view your stats.")
            return

        # Step 1: Generate ability scores
        ability_scores = {
            "Strength": random.randint(3, 18),
            "Dexterity": random.randint(3, 18),
            "Constitution": random.randint(3, 18),
            "Intelligence": random.randint(3, 18),
            "Wisdom": random.randint(3, 18),
            "Charisma": random.randint(3, 18)
        }

        # Calculate HP based on Constitution modifier
        con_modifier = (ability_scores["Constitution"] - 10) // 2
        hp = max(10 + con_modifier, 1)

        def format_ability_scores():
            return (
                f"💪 Strength: {ability_scores['Strength']}\n"
                f"🏹 Dexterity: {ability_scores['Dexterity']}\n"
                f"🛡️ Constitution: {ability_scores['Constitution']}\n"
                f"🧠 Intelligence: {ability_scores['Intelligence']}\n"
                f"👁️ Wisdom: {ability_scores['Wisdom']}\n"
                f"🗣️ Charisma: {ability_scores['Charisma']}\n"
                f"❤️ HP: {hp}"
            )

        await message.channel.send(
            f"🎲 **Rolling your ability scores...**\n\n"
            f"{format_ability_scores()}\n\n"
            "💡 Now, what is your **character's name**?\n"
            "Reply with a name or type **`random`** to generate one."
        )

        # Step 2: Choose Name
        try:
            def check(m):
                return m.author == message.author and m.channel == message.channel

            name_response = await client.wait_for("message", check=check, timeout=30.0)
            character_name = name_response.content.strip().title() if name_response.content.lower() != "random" else random.choice(FANTASY_NAMES)

        except asyncio.TimeoutError:
            character_name = random.choice(FANTASY_NAMES)

        await message.channel.send(
            f"🏰 Great! Your character's name is **{character_name}**.\n"
            "Now, choose a **race** or type **`random`** to get one."
        )

        # Step 3: Choose Race
        try:
            race_response = await client.wait_for("message", check=check, timeout=30.0)
            character_race = race_response.content.strip().title() if race_response.content.lower() != "random" else random.choice(RACES)

        except asyncio.TimeoutError:
            character_race = random.choice(RACES)

        await message.channel.send(
            f"🌍 You have chosen **{character_race}** as your race.\n"
            "Now, choose a **class** based on your ability scores above, or type **`random`** to get one."
        )

        # Step 4: Choose Class
        try:
            class_response = await client.wait_for("message", check=check, timeout=30.0)
            character_class = class_response.content.strip().title() if class_response.content.lower() != "random" else random.choice(CLASSES)

        except asyncio.TimeoutError:
            character_class = random.choice(CLASSES)

        await message.channel.send(
            f"🎭 You are now **{character_name} the {character_race} {character_class}**!\n"
            "Lastly, choose **3 skills** for proficiency from the following list:\n"
            "`acrobatics, animal handling, arcana, athletics, deception, history, insight, intimidation, investigation, medicine, nature, perception, performance, persuasion, religion, sleight of hand, stealth, survival`"
            "\nReply with **3 skills** separated by commas (e.g., `stealth, perception, athletics`)."
        )

        # Step 5: Choose Proficiencies
        try:
            response = await client.wait_for("message", check=check, timeout=60.0)
            chosen_skills = [skill.strip().lower() for skill in response.content.split(",")]

            if len(chosen_skills) != 3:
                await message.channel.send("❌ Invalid selection! Restart `!register` and choose **exactly 3 skills**.")
                return

        except asyncio.TimeoutError:
            await message.channel.send("⏳ Registration timed out! Run `!register` again.")
            return

        # Store player data
        player_stats[user_id_str] = {
            "Name": character_name,
            "Race": character_race,
            "Class": character_class,
            **ability_scores,
            "HP": hp,
            "proficiencies": chosen_skills,
            "history": []
        }

        save_players()

        await message.channel.send(
            f"🎉 **Registration Complete!**\n"
            f"🏰 **{character_name} the {character_race} {character_class}** has been created!\n"
            "Use `!stats` to view your full character details!"
        )

    # ----- RESET PLAYER STATS: !reset -----
    if message.content.startswith("!reset"):
        user_id_str = str(message.author.id)

        if user_id_str not in player_stats:
            await message.channel.send("❌ You do not have a registered character to reset.")
            return

        await message.channel.send(
            f"⚠️ {message.author.mention}, this will **permanently delete** your character! "
            "If you'd like to proceed, type **`confirm`**. Type **`cancel`** to abort."
        )

        try:
            def check(m):
                return m.author == message.author and m.channel == message.channel

            response = await client.wait_for("message", check=check, timeout=30.0)  # 30-second timeout
            user_input = response.content.lower()

            if user_input == "confirm":
                # Save character to the graveyard before deleting
                save_to_graveyard(user_id_str, player_stats[user_id_str])

                # Delete character from active player stats
                del player_stats[user_id_str]
                save_players()

                await message.channel.send(
                    f"💀 Your character has been **deleted** and moved to the **Character Graveyard**.\n"
                    "You can now use `!register` to start fresh!"
                )
        
            elif user_input == "cancel":
                await message.channel.send("❌ Character reset **canceled**. Your character remains intact.")

            else:
                await message.channel.send("❌ Invalid response! Reset **aborted**. Run `!reset` again if you still wish to delete your character.")

        except asyncio.TimeoutError:
            await message.channel.send("⏳ Reset request timed out. Your character remains intact.")

    # ----- VIEW PLAYER STATS: !stats -----
    elif message.content.startswith("!stats"):
        user_id_str = str(message.author.id)

        if user_id_str not in player_stats:
            await message.channel.send("❌ You are not registered! Use `!register` to create a character.")
            return

        stats = player_stats[user_id_str]

        def calc_modifier(score):
            return (score - 10) // 2

        stats_message = (
            f"🏰 **{stats.get('Name')} the {stats.get('Race')} {stats.get('Class')}**\n"
            f"💪 Strength: {stats['Strength']} (mod: {calc_modifier(stats['Strength']):+})\n"
            f"🏹 Dexterity: {stats['Dexterity']} (mod: {calc_modifier(stats['Dexterity']):+})\n"
            f"🛡️ Constitution: {stats['Constitution']} (mod: {calc_modifier(stats['Constitution']):+})\n"
            f"🧠 Intelligence: {stats['Intelligence']} (mod: {calc_modifier(stats['Intelligence']):+})\n"
            f"👁️ Wisdom: {stats['Wisdom']} (mod: {calc_modifier(stats['Wisdom']):+})\n"
            f"🗣️ Charisma: {stats['Charisma']} (mod: {calc_modifier(stats['Charisma']):+})\n"
            f"❤️ HP: {stats['HP']}\n"
            f"🎖️ Proficiencies: {', '.join(stats['proficiencies']).title()}"
        )

        await message.channel.send(stats_message)

    # ----- VIEW PAST PLAYER CHARACTERS: !graveyard -----
    elif message.content.startswith("!graveyard"):
        user_id_str = str(message.author.id)

        # Check if the graveyard file exists
        if not os.path.exists(GRAVEYARD_FILE):
            await message.channel.send("💀 The Character Graveyard is empty. No past characters found.")
            return

        # Load graveyard data
        with open(GRAVEYARD_FILE, "r") as f:
            graveyard = json.load(f)

        if user_id_str not in graveyard:
            await message.channel.send("💀 You have no past characters in the Graveyard.")
            return

        # Retrieve the past character
        past_character = graveyard[user_id_str]

        def calc_modifier(score):
            return (score - 10) // 2

        # Format the character's info
        graveyard_message = (
            f"🕯️ **Past Character Found!**\n"
            f"🏰 **{past_character.get('Name')} the {past_character.get('Race')} {past_character.get('Class')}**\n"
            f"💪 Strength: {past_character['Strength']} (mod: {calc_modifier(past_character['Strength']):+})\n"
            f"🏹 Dexterity: {past_character['Dexterity']} (mod: {calc_modifier(past_character['Dexterity']):+})\n"
            f"🛡️ Constitution: {past_character['Constitution']} (mod: {calc_modifier(past_character['Constitution']):+})\n"
            f"🧠 Intelligence: {past_character['Intelligence']} (mod: {calc_modifier(past_character['Intelligence']):+})\n"
            f"👁️ Wisdom: {past_character['Wisdom']} (mod: {calc_modifier(past_character['Wisdom']):+})\n"
            f"🗣️ Charisma: {past_character['Charisma']} (mod: {calc_modifier(past_character['Charisma']):+})\n"
            f"❤️ HP: {past_character['HP']}\n"
            f"🎖️ Proficiencies: {', '.join(past_character['proficiencies']).title()}"
        )

        await message.channel.send(graveyard_message)

    # ----- VIEW PLAYER SKILLS: !skills -----
    elif message.content.startswith("!skills"):
        skill_list = (
            "**Available Skills & Associated Abilities:**\n"
            "🌀 Acrobatics (Dexterity) | 🐾 Animal Handling (Wisdom) | 📖 Arcana (Intelligence)\n"
            "🏋️ Athletics (Strength) | 🎭 Deception (Charisma) | 🏛️ History (Intelligence)\n"
            "👁️ Insight (Wisdom) | 😈 Intimidation (Charisma) | 🔍 Investigation (Intelligence)\n"
            "🩺 Medicine (Wisdom) | 🌿 Nature (Intelligence) | 👀 Perception (Wisdom)\n"
            "🎶 Performance (Charisma) | 🗣️ Persuasion (Charisma) | 🔥 Religion (Intelligence)\n"
            "🤹 Sleight of Hand (Dexterity) | 🥷 Stealth (Dexterity) | 🏕️ Survival (Wisdom)\n\n"
        )
        await message.channel.send(skill_list)

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
    # ------------------- Context-Specific Roll Commands -------------------

    # Melee Attack Roll - uses Strength modifier
    elif message.content.startswith("!attack"):
        cooldown_time = 3  # 3-second cooldown for attack rolls
        remaining = is_on_cooldown(user_id, "!attack", cooldown_time)
        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before attacking again.")
            return
        set_cooldown(user_id, "!attack", cooldown_time)
        roll = random.randint(1, 20)
        user_id_str = str(message.author.id)
        if user_id_str in player_stats:
            score = player_stats[user_id_str].get("Strength", 10)
            bonus = (score - 10) // 2
            final_total = roll + bonus
            bonus_str = f" (+{bonus})" if bonus >= 0 else f" ({bonus})"
            await message.channel.send(
                f"⚔️ **Attack Roll:** You rolled a **{roll}**{bonus_str} (1d20) using your Strength modifier for a total of **{final_total}**!"
            )
        else:
            await message.channel.send(
                f"⚔️ **Attack Roll:** You rolled a **{roll}** (1d20)! Register with `!register` to gain stat bonuses."
            )

    # Ranged Attack Roll - uses Dexterity modifier
    elif message.content.startswith("!ranged"):
        cooldown_time = 3  # 3-second cooldown for ranged attacks
        remaining = is_on_cooldown(user_id, "!ranged", cooldown_time)
        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before making a ranged attack.")
            return
        set_cooldown(user_id, "!ranged", cooldown_time)
        roll = random.randint(1, 20)
        user_id_str = str(message.author.id)
        if user_id_str in player_stats:
            score = player_stats[user_id_str].get("Dexterity", 10)
            bonus = (score - 10) // 2
            final_total = roll + bonus
            bonus_str = f" (+{bonus})" if bonus >= 0 else f" ({bonus})"
            await message.channel.send(
                f"🏹 **Ranged Attack Roll:** You rolled a **{roll}**{bonus_str} (1d20) using your Dexterity modifier for a total of **{final_total}**!"
            )
        else:
            await message.channel.send(
                f"🏹 **Ranged Attack Roll:** You rolled a **{roll}** (1d20)! Register with `!register` to gain stat bonuses."
            )

    # Saving Throw Roll - expects an ability parameter (e.g., !save Constitution)
    elif message.content.startswith("!save"):
        cooldown_time = 3  # 3-second cooldown for saving throws
        remaining = is_on_cooldown(user_id, "!save", cooldown_time)
        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before rolling another saving throw.")
            return
        set_cooldown(user_id, "!save", cooldown_time)
        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("❌ Please specify which saving throw to roll (e.g., `!save Constitution`).")
            return
        ability = parts[1].capitalize()
        if ability not in {"Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"}:
            await message.channel.send("❌ Invalid ability specified. Choose from Strength, Dexterity, Constitution, Intelligence, Wisdom, or Charisma.")
            return
        roll = random.randint(1, 20)
        user_id_str = str(message.author.id)
        if user_id_str in player_stats:
            score = player_stats[user_id_str].get(ability, 10)
            bonus = (score - 10) // 2
            final_total = roll + bonus
            bonus_str = f" (+{bonus})" if bonus >= 0 else f" ({bonus})"
            await message.channel.send(
                f"🛡️ **Saving Throw ({ability}):** You rolled a **{roll}**{bonus_str} (1d20) for a total of **{final_total}**!"
            )
        else:
            await message.channel.send(
                f"🛡️ **Saving Throw:** You rolled a **{roll}** (1d20)! Register with `!register` to gain stat bonuses."
            )

    # Skill Check Roll - expects a skill parameter (e.g., !skill Stealth)
    elif message.content.startswith("!skill"):
        cooldown_time = 3  # 3-second cooldown for skill checks
        remaining = is_on_cooldown(user_id, "!skill", cooldown_time)
        if remaining:
            await message.channel.send(f"⏳ You must wait {remaining} seconds before making another skill check.")
            return
        set_cooldown(user_id, "!skill", cooldown_time)

        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("To roll a skill check, type `!skill <skill_name>` (e.g., `!skill Stealth`).")
            return

        # Skill-to-Ability Mapping (Based on D&D 5e rules)
        skill_map = {
            "acrobatics": "Dexterity",
            "animal handling": "Wisdom",
            "arcana": "Intelligence",
            "athletics": "Strength",
            "deception": "Charisma",
            "history": "Intelligence",
            "insight": "Wisdom",
            "intimidation": "Charisma",
            "investigation": "Intelligence",
            "medicine": "Wisdom",
            "nature": "Intelligence",
            "perception": "Wisdom",
            "performance": "Charisma",
            "persuasion": "Charisma",
            "religion": "Intelligence",
            "sleight of hand": "Dexterity",
            "stealth": "Dexterity",
            "survival": "Wisdom",
        }

        # Extract skill name and normalize it
        skill_input = " ".join(parts[1:]).lower()
        if skill_input not in skill_map:
            await message.channel.send("❌ Invalid skill specified. Use `!skills` to see the full list.")
            return

        ability = skill_map[skill_input]  # Get the associated ability score
        roll = random.randint(1, 20)
        user_id_str = str(message.author.id)

        if user_id_str in player_stats:
            score = player_stats[user_id_str].get(ability, 10)
            bonus = (score - 10) // 2
            final_total = roll + bonus
            bonus_str = f" (+{bonus})" if bonus >= 0 else f" ({bonus})"
            await message.channel.send(
                f"📜 **{skill_input.capitalize()} Check ({ability}):** You rolled a **{roll}**{bonus_str} (1d20) for a total of **{final_total}**!"
            )
        else:
            await message.channel.send(
                f"📜 **Skill Check:** You rolled a **{roll}** (1d20)! Register with `!register` to gain stat bonuses."
            )

# ------------------ Run the Discord Bot ------------------

client.run(DISCORD_TOKEN)
