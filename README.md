# 🎲 AI-Powered D&D Scenario Bot

**A Discord bot that generates dynamic D&D adventure scenarios, letting players experience interactive narratives with traditional RPG mechanics.**

---

## Overview

The **AI-Powered D&D Scenario Bot** blends **AI-generated adventures** with **Dungeons & Dragons 5e mechanics**. Players can roll dice, make decisions that impact the story, and interact with a fully fleshed-out character system.

---

## 📌 Features

- **AI-Generated Adventures:**  
  Create unique scenarios using GPT-3.5-Turbo for adventure hooks and GPT-4 for decision outcomes.
  
- **Interactive Choices:**  
  Progress your adventure using `!choose 1/2/3`.

- **Full D&D 5e Character Stats & Customization:**  
  - Players **name their characters** or **generate a random fantasy name**.  
  - Choose from **multiple fantasy races** (e.g., Elf, Dwarf, Tiefling).  
  - Select a **class** (e.g., Fighter, Wizard, Rogue) based on **rolled ability scores**.  
  - **Proficiency Selection:** Players **pick 3 skills** during registration.  
  - HP is dynamically calculated using Constitution.

- **Expanded Dice Rolling System:**  
  - `!roll d20` → Rolls a **d20** with **no modifier**.  
  - `!roll d20 <ability>` → Rolls a **d20 + ability modifier** (Strength, Dexterity, etc.).  
  - `!attack` → Rolls a melee attack (Strength modifier).  
  - `!ranged` → Rolls a ranged attack (Dexterity modifier).  
  - `!save <ability>` → Rolls a saving throw (e.g., `!save Wisdom`).  
  - `!skill <skill_name>` → Rolls a skill check using the correct ability modifier.  
  - `!skills` → Lists all available skills and their linked abilities.

- **Decision Tracking & Persistence:**  
  - Choices made using `!choose` are stored in a **SQLite database**.  
  - Decisions may impact future adventures!

- **Character Reset & Graveyard System:**  
  - `!reset` allows players to **delete their current character and start fresh**.  
  - Deleted characters are **stored in `graveyard.json`** and can be viewed with `!graveyard`.  
  - `!graveyard` allows players to **retrieve past character data**.

- **Optimized API Usage:**  
  Incorporates caching and rate-limiting to reduce API costs.
  
- **Hybrid AI Model:**  
  Combines GPT-3.5 for general content and GPT-4 for more nuanced decision outcomes.

---

## 🚀 Getting Started

### Prerequisites

Before running the bot, ensure you have:
- **Python 3.8+** installed.
- A **Discord Developer Account** and a **Discord Bot Token** ([Create Here](https://discord.com/developers/applications)).
- An **OpenAI API Key** ([Get One Here](https://platform.openai.com/signup)).
- Dependencies installed via:
  ```bash
  pip install -r requirements.txt

---

### 2️⃣ Installation & Setup

#### **Step 1: Clone the Repository**
```bash
git clone https://github.com/YOUR-USERNAME/ai-dnd-scenario-bot.git
cd ai-dnd-scenario-bot
```

#### **Step 2: Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

#### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **Step 4: Set Up API Keys**
1. **Create a `.env` file** in the project folder:
```ini
DISCORD_TOKEN=your-discord-bot-token-here
OPENAI_API_KEY=your-openai-api-key-here
```
2. **Save the file** (This keeps your keys secure!).

---

### 3️⃣ Running the Bot
```bash
python bot.py
```
✅ The bot will log in to Discord and wait for commands!

---

## 🎮 How to Play

### 🔹 Available Commands
| Command | Description |
|---------|-------------|
| `!register` | Registers a new character (name, race, class, ability scores, proficiencies). |
| `!stats` | Displays your character's Name, Race, Class, ability scores, and proficiencies. |
| `!adventure` | Generates a new AI-powered adventure scenario. |
| `!choose 1/2/3` | Selects an adventure path based on the choices provided. |
| `!reset` | Deletes your character (with confirmation) and allows re-registration. |
| `!graveyard` | Displays the last deleted character from the Character Graveyard. |
| `!roll d20` | Rolls a d20 without any modifier. |
| `!roll d20 <ability>` | Rolls a d20 + ability modifier (Strength, Dexterity, Constitution, etc.). |
| `!attack` | Rolls a melee attack (Strength modifier). |
| `!ranged` | Rolls a ranged attack (Dexterity modifier). |
| `!save <ability>` | Rolls a saving throw (e.g., `!save Wisdom`). |
| `!skills` | 	Displays the full list of available skills and their linked abilities. |
| `!skill <skill_name>` | Rolls a skill check using the correct ability modifier (e.g., `!skill Perception`). |

### 📖 Usage Example
```yaml
User: !register
Bot: 🎲 Rolling your ability scores...
     💪 Strength: 14
     🏹 Dexterity: 12
     🛡️ Constitution: 16
     🧠 Intelligence: 10
     👁️ Wisdom: 8
     🗣️ Charisma: 15
     ❤️ HP: 13
     
     💡 What is your **character's name**?
     Reply with a name or type `random` to generate one.

User: Kael  
Bot: 🏰 Great! Your character's name is **Kael**.
     Now, choose a **race** or type `random` to get one.

User: Elf  
Bot: 🌍 You have chosen **Elf** as your race.
     Now, choose a **class** based on your ability scores above, or type `random` to get one.

User: Ranger  
Bot: 🎭 You are now **Kael the Elf Ranger**!
     Lastly, choose **3 skills** for proficiency from the following list:
     `acrobatics, animal handling, arcana, athletics, deception, history, insight, intimidation, investigation, medicine, nature, perception, performance, persuasion, religion, sleight of hand, stealth, survival`
     Reply with **3 skills** separated by commas (e.g., `stealth, perception, athletics`).

User: stealth, perception, athletics  
Bot: ✅ Kael has been registered with the following stats:
     💪 Strength: 14 (mod: +2)
     🏹 Dexterity: 12 (mod: +1)
     🛡️ Constitution: 16 (mod: +3)  --> ❤️ HP: 13 (base 10 + +3)
     🧠 Intelligence: 10 (mod: +0)
     👁️ Wisdom: 8 (mod: -1)
     🗣️ Charisma: 15 (mod: +2)
     🎖️ Proficiencies: **Stealth, Perception, Athletics**
     Use `!stats` to view your character's full details.

User: !stats  
Bot: 📜 **Kael the Elf Ranger**
     💪 Strength: 14 (mod: +2)
     🏹 Dexterity: 12 (mod: +1)
     🛡️ Constitution: 16 (mod: +3)
     🧠 Intelligence: 10 (mod: +0)
     👁️ Wisdom: 8 (mod: -1)
     🗣️ Charisma: 15 (mod: +2)
     ❤️ HP: 13
     🎖️ Proficiencies: **Stealth, Perception, Athletics**

User: !roll d20  
Bot: 🎲 You rolled a **15** (1d20) with no modifier!

User: !roll d20 dexterity  
Bot: 🎲 You rolled a **15** (+1) (1d20) using your Dexterity modifier for a total of **16**!

User: !attack  
Bot: ⚔️ **Attack Roll:** You rolled a **12** (+2) (1d20) using your Strength modifier for a total of **14**!

User: !ranged  
Bot: 🏹 **Ranged Attack Roll:** You rolled a **17** (+1) (1d20) using your Dexterity modifier for a total of **18**!

User: !save wisdom  
Bot: 🛡️ **Saving Throw (Wisdom):** You rolled a **9** (-1) (1d20) for a total of **8**!

User: !skill stealth  
Bot: 📜 **Stealth Check (Dexterity):** You rolled a **13** (+1) (1d20) for a total of **14**!

User: !adventure  
Bot: 🎲 Generating a new adventure... please wait!
     📜 **Adventure Hook:**
     A mysterious cave beckons in the dark forest...
     ⚔️ **Choices:**
     1️⃣ Enter the cave.
     2️⃣ Circumvent the cave.
     3️⃣ Set up camp nearby.
     Use `!choose 1`, `!choose 2`, or `!choose 3` to decide your action!

User: !choose 1  
Bot: 🔮 You chose: Enter the cave.
     🎲 Your roll: 14
     📝 **Outcome:** As you step into the cave, you discover ancient inscriptions...

User: !reset  
Bot: ⚠️ This will **permanently delete** your character! If you'd like to proceed, type **`confirm`**.

User: confirm  
Bot: 💀 Your character has been **deleted** and moved to the **Character Graveyard**.
     You can now use `!register` to start fresh!

User: !graveyard  
Bot: 🕯️ **Past Character Found!**
     🏰 **Kael the Elf Ranger**
     💪 Strength: 14 (mod: +2)
     🏹 Dexterity: 12 (mod: +1)
     🛡️ Constitution: 16 (mod: +3)
     🧠 Intelligence: 10 (mod: +0)
     👁️ Wisdom: 8 (mod: -1)
     🗣️ Charisma: 15 (mod: +2)
     ❤️ HP: 13
     🎖️ Proficiencies: **Stealth, Perception, Athletics**
```
---
## 🛠 Technologies & Dependencies
- **Python 3.8+**
- **Discord.py** for interacting with the Discord API
- **OpenAI API** for generating AI content
- **dotenv** for environment variable management

---
## ⚠️ Known Issues
- Adventure caching may occasionally reuse outdated choices.
- `!graveyard` currently only retrieves the most recent deleted character. Future updates may allow retrieval of multiple past characters.
- Further refinement of context-specific roll commands (e.g., adding proficiency bonuses) is planned.
- Additional testing required for edge cases (e.g., unregistered users using modifier commands).

---
## 🤝 Contributing
Contributions are welcome! Please follow these guidelines:
- **Code Style:** Follow PEP8 guidelines and ensure your code is well-commented.
- **Pull Requests:** Submit a clear PR with detailed descriptions of changes and reference any related issues.
- **Testing:** Ensure your changes are tested locally before submission.
- **Documentation**: Update the README and inline documentation if your changes affect functionality.

Feel free to fork the repository, experiment, and propose enhancements via the Issues tab.

---

## 📜 License
MIT License. Feel free to modify and expand!

---

## 🌟 Credits
Created by **Professor_Alex** and contributors.  
Special thanks to **ChatGPT (by OpenAI)** for providing technical guidance, optimizations, and brainstorming.