# 🎲 AI-Powered D&D Scenario Bot

**A Discord bot that generates dynamic D&D adventure scenarios, letting players experience interactive narratives with traditional RPG mechanics.**

---

## Overview

AI-Powered D&D Scenario Bot creates unique D&D adventures on Discord by leveraging OpenAI's GPT models. The bot not only generates engaging adventure hooks and interactive choices but also incorporates authentic D&D 5e mechanics—such as full character ability scores, dynamic HP calculations, and context-sensitive dice rolls.

---

## 📌 Features

- **AI-Generated Adventures:**  
  Create unique scenarios using GPT-3.5-Turbo for adventure hooks and GPT-4 for decision outcomes.
  
- **Interactive Choices:**  
  Progress your adventure with commands like `!choose 1/2/3`.

- **Full D&D 5e Character Stats:**  
  Register a character with six ability scores—**Strength, Dexterity, Constitution, Intelligence, Wisdom, and Charisma**.  
  - HP is dynamically calculated using your Constitution modifier.
  
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
| `!register` | Registers a new character with full D&D 5e stats and dynamically calculated HP. |
| `!stats` | Displays your character's six ability scores, their modifiers, and your current HP. |
| `!adventure` | Generates a new AI-powered adventure scenario. |
| `!choose 1/2/3` | Selects an adventure path based on the choices provided. |
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
Bot: @Player, you have been registered with the following stats:
     💪Strength: 14 (mod: +2)
     🏹Dexterity: 12 (mod: +1)
     🛡️Constitution: 16 (mod: +3)  --> ❤️HP: 13 (base 10 + +3)
     🧠Intelligence: 10 (mod: +0)
     👁️Wisdom: 8 (mod: -1)
     🗣️Charisma: 15 (mod: +2)
     Use `!stats` to view your character's attributes.

User: !stats
Bot: 📜 **Player's Stats:**
     💪Strength: 14 (mod: +2)
     🏹Dexterity: 12 (mod: +1)
     🛡️Constitution: 16 (mod: +3)
     🧠Intelligence: 10 (mod: +0)
     👁️Wisdom: 8 (mod: -1)
     🗣️Charisma: 15 (mod: +2)
     ❤️ HP: 13

User: !roll d20
Bot: 🎲 You rolled a **15** (1d20) with no modifier!

User: !roll d20 dexterity
Bot: 🎲 You rolled a **15** (+1) (1d20) using your Dexterity modifier for a total of **16**!

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
- Further refinement of context-specific roll commands (e.g., adding proficiency bonuses) is planned.
- Additional testing is required for unregistered users using modifier commands.
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